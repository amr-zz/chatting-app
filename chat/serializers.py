from .models import Message, Conversation
from rest_framework import serializers



class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(source='conversation.id', read_only=True)
    message_sender = serializers.CharField(source='message_sender.username', read_only=True)
    message_sender_id = serializers.IntegerField(source='message_sender.id', read_only=True)
    conversation = serializers.CharField(source='conversation.conversation_name', read_only=True)
    message_sent_at = serializers.DateTimeField(read_only=True, format="%Y/%m/%d %H:%M")
    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'message_content',
            'message_sender',
            'conversation_id',
            'message_sender_id',
            'message_sent_at'
        ]
        read_only_fields = ['message_sender','conversation','conversation_id','message_sender_id','message_sent_at']



class ConversationSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    conversation_created_by = serializers.CharField(source='conversation_created_by.username', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    members = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = [
            'id',
            'conversation_name',
            'conversation_description',
            'conversation_created_by',
            'members',
            'messages',
            'member_count',
        ]
        read_only_fields = ['messages','conversation_created_by']

    def get_member_count(self,obj):
        return obj.members.count()
    
    def get_members(self,obj):
        members = []
        for member in obj.members.all():
            members.append({"username": member.username,
                            "profile_image": member.profile_image.url})
        return members
    
    def create(self,validated_data):
        members_data = validated_data.pop('members',[])
        user = self.context['request'].user
        if user not in members_data:
            members_data.append(user)
        conversation = Conversation.objects.create(
            conversation_name=validated_data['conversation_name'],
            conversation_description=validated_data['conversation_description'],
            conversation_created_by=user,
        )
        conversation.members.set(members_data)
        conversation.messages.set([])
        return conversation