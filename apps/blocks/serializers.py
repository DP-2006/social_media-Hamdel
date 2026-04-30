# apps/blocks/serializers.py

from django.conf import settings
from rest_framework import serializers
from .models import Block

class BlockSerializer(serializers.ModelSerializer):    
    blocker_username = serializers.CharField(source='blocker.username', read_only=True)
    blocked_username = serializers.CharField(source='blocked.usernam         e', read_only=True)
    blocked_phone = serializers.CharField(source='blocked.phone', read_only=True)
    class Meta:
        model = Block
        fields = [

            'id', 'blocker', 'blocker_username', 
            'blocked', 'blocked_username', 'blocked_phone',
            'reason', 'created_at'

        ]
        read_only_fields = ['id', 'created_at']


class BlockedUserSerializer(serializers.ModelSerializer):
    
    blocked_at = serializers.DateTimeField(source='blocked_info.created_at', read_only=True)
    block_reason = serializers.CharField(source='blocked_info.reason', read_only=True)
    
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'phone', 'blocked_at', 'block_reason']

class BlockRequestSerializer(serializers.Serializer):

    user_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)


