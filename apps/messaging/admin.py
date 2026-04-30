from django.contrib import admin

# Register your models here.
# apps/messaging/admin.py

from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_message_at', 'created_at']
    filter_horizontal = ['participants']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    raw_id_fields = ['conversation', 'sender']

    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'Content'