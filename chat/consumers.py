from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from channels.db import database_sync_to_async
from django.shortcuts import redirect

import json



class ConversationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        """Called when the websocket is connected."""

        if self.scope.get('error') == 'Invalid token':
            await self.accept()
            await self.close(4001, 'invalid token')
            return
        
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_name = self.scope['url_route']['kwargs']['conversation_name']
        self.group_name = f'conversation_{self.conversation_id}'
            
        users = await self.get_conversation_users(self.conversation_id)
        if self.scope['user'] not in users:
            await self.accept()
            await self.close(4005, 'not in conversation')

        else:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({"type": "username","username": self.scope['user'].username}))

    async def disconnect(self, close_code):
        """Called when the websocket is disconnected."""
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        """Called when Recieving anything from the websocket."""
        data = json.loads(text_data)
        message = data.get('message',None)
        sender = self.scope['user'].username

        if data.get('type') == 'conversation_message' and message is not None:
            # save the message to the db
            await self.save_message(self.conversation_id, self.scope['user'], message)

            # send the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'conversation_message',
                    'message': message,
                    'sender': sender
                }
            )
        
        elif data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'typing',
                    'sender': sender
                }
            )

        elif data.get('type') == 'edit_message':
            updated = await self.edit_message_in_db(data['message_id'], data['new_content'])
            if updated:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'edit_message',
                        'message_id': data['message_id'],
                        'new_content': data['new_content']
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'failed to edit.'
                }))
        elif data.get('type') == 'delete_message':
            deleted = await self.delete_message_in_db(data['message_id'])

            if deleted:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'delete_message',
                        'message_id': data['message_id']
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'failed to delete.'
                }))

    async def conversation_message(self, event):
        """Called when a message is sent to the websocket."""
        await self.send(text_data=json.dumps({
            'type': 'conversation_message',
            'message': event['message'],
            'sender': event['sender']
        }))

    async def typing(self, event):
        """Called when a typing event is sent to the websocket."""
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': event['sender']
        }))

    async def edit_message(self, event):
        """Called when a message is edited."""
        await self.send(text_data=json.dumps({
            'type': 'edit_message',
            'message_id': event['message_id'],
            'new_content': event['new_content']
        }))
    
    async def delete_message(self, event):
        """Called when a message is deletd."""
        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, sender, message):
        conversation = Conversation.objects.get(id=conversation_id)
        Message.objects.create(
            conversation=conversation,
            message_content=message,
            message_sender=sender
        )
    
    @database_sync_to_async
    def get_conversation_users(self, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return []
        return list(conversation.members.all())
    
    @database_sync_to_async
    def edit_message_in_db(self, message_id, new_content):
        try:
            message = Message.objects.get(id=message_id, message_sender=self.scope['user'])
            message.message_content = new_content
            message.save()
            return True
        except Message.DoesNotExist:
            return False
        
    @database_sync_to_async
    def delete_message_in_db(self, message_id):
        try:
            message = Message.objects.get(id=message_id, message_sender=self.scope['user'])
            message.delete()
            return True
        except Message.DoesNotExist:
            return False

        

    