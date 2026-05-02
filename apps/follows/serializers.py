# apps/follows/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    """سریالایزر اصلی فالو"""
    
    follower_id = serializers.UUIDField(source='follower.id', read_only=True)
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    follower_display_name = serializers.SerializerMethodField()
    follower_profile_image = serializers.SerializerMethodField()
    
    following_id = serializers.UUIDField(source='following.id', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    following_display_name = serializers.SerializerMethodField()
    following_profile_image = serializers.SerializerMethodField()
    
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Follow
        fields = [
            'id', 'created_at',
            'follower_id', 'follower_username', 'follower_display_name', 'follower_profile_image',
            'following_id', 'following_username', 'following_display_name', 'following_profile_image'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_follower_display_name(self, obj):
        if hasattr(obj.follower, 'profile') and obj.follower.profile:
            return obj.follower.profile.display_name or obj.follower.username
        return obj.follower.username
    
    def get_follower_profile_image(self, obj):
        if hasattr(obj.follower, 'profile') and obj.follower.profile and obj.follower.profile.profile_image:
            return obj.follower.profile.profile_image.url
        return None
    
    def get_following_display_name(self, obj):
        if hasattr(obj.following, 'profile') and obj.following.profile:
            return obj.following.profile.display_name or obj.following.username
        return obj.following.username
    
    def get_following_profile_image(self, obj):
        if hasattr(obj.following, 'profile') and obj.following.profile and obj.following.profile.profile_image:
            return obj.following.profile.profile_image.url
        return None


class FollowerListSerializer(serializers.Serializer):
    """سریالایزر لیست فالوورها (ساده)"""
    id = serializers.UUIDField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    profile_image = serializers.CharField(allow_null=True)
    followed_at = serializers.DateTimeField()


class FollowingListSerializer(serializers.Serializer):
    """سریالایزر لیست فالوینگ‌ها (ساده)"""
    id = serializers.UUIDField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    profile_image = serializers.CharField(allow_null=True)
    followed_at = serializers.DateTimeField()