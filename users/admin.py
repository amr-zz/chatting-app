from django.contrib import admin
from users.models import MyUser
from chat.models import Conversation, Message

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_name', 'conversation_description', 'conversation_created_by', 'created_at')
    search_fields = ('conversation_name', 'conversation_description', 'conversation_created_by__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation__conversation_name', 'message_content', 'message_sender', 'message_sent_at')
    search_fields = ('conversation__conversation_name', 'message_content', 'message_sender__username')

admin.site.register(MyUser, UserAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)