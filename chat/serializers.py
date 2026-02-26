from .models import Message, Conversation
from rest_framework import serializers



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = [
            'id',
            'conversation_name',
            'conversation_description',
            'conversation_created_by',
            'members',
            'messages',
            'member_count'
        ]
        read_only_fields = ['messages']

    def get_member_count(self,obj):
        return obj.members.count()
    
    def create(self,validated_data):
        members_data = validated_data.pop('members',[])
        creator = validated_data['conversation_created_by']
        if creator not in members_data:
            members_data.append(creator)
        conversation = Conversation.objects.create(
            conversation_name=validated_data['conversation_name'],
            conversation_description=validated_data['conversation_description'],
            conversation_created_by=validated_data['conversation_created_by'],
        )
        conversation.members.set(members_data)
        conversation.messages.set([])
        return conversation