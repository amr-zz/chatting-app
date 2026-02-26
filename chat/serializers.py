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
        read_only_fields = ['messages','conversation_created_by']

    def get_member_count(self,obj):
        return obj.members.count()
    
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