# apps/messaging/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """سریالایزر ساده کاربر"""
    display_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'profile_image']
    
    def get_display_name(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.display_name or obj.username
        return obj.username
    
    def get_profile_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile and obj.profile.profile_image:
            return obj.profile.profile_image.url
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at', 'is_read', 'is_mine']
        read_only_fields = ['id', 'created_at', 'is_read']
    
    def get_is_mine(self, obj):
        request = self.context.get('request')
        if request and obj.sender == request.user:
            return True
        return False


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserMinimalSerializer(many=True, read_only=True)
    other_participant = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'other_participant', 'last_message', 
                  'last_message_at', 'unread_count', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_message_at']
    
    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request:
            other = obj.participants.exclude(id=request.user.id).first()
            if other:
                return UserMinimalSerializer(other).data
        return None
    
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        if last:
            return MessageSerializer(last, context=self.context).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0