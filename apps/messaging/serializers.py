# apps/messaging/serializers.py

from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'is_read', 'read_at', 'created_at']
        read_only_fields = ['id', 'sender', 'is_read', 'read_at', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'unread_count', 'last_message_at', 'created_at']
        read_only_fields = ['id', 'last_message_at', 'created_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(
                sender__not=request.user,
                is_read=False
            ).count()
        return 0