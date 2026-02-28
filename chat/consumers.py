from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from channels.db import database_sync_to_async
import json



class ConversationConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        """Called when the websocket is connected."""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_name = self.scope['url_route']['kwargs']['conversation_name']
        self.group_name = f'conversation_{self.conversation_id}'


        users = await self.get_conversation_users(self.conversation_id)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Called when the websocket is disconnected."""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Called when Recieving a message from the websocket."""
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user'].username

        if data.get('type') == 'conversation_message':
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
        return conversation.members.all()





        

    