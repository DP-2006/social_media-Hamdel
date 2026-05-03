# apps/follows/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


class FollowerListSerializer(serializers.ModelSerializer):
    """
    سریالایزر لیست فالوورها - نمایش اطلاعات کاربر فالوکننده
    """
    id = serializers.IntegerField(source='follower.id', read_only=True)
    username = serializers.CharField(source='follower.username', read_only=True)
    email = serializers.EmailField(source='follower.email', read_only=True)
    followed_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'username', 'email', 'followed_at']


class FollowingListSerializer(serializers.ModelSerializer):
    """
    سریالایزر لیست فالوهای کاربر - نمایش اطلاعات کاربر فالوشونده
    """
    id = serializers.IntegerField(source='following.id', read_only=True)
    username = serializers.CharField(source='following.username', read_only=True)
    email = serializers.EmailField(source='following.email', read_only=True)
    followed_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'username', 'email', 'followed_at']


class FollowSerializer(serializers.ModelSerializer):
    """
    سریالایزر کامل برای استفاده در جزئیات
    """
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'follower_username', 
                  'following_username', 'created_at']
        read_only_fields = ['id', 'created_at']