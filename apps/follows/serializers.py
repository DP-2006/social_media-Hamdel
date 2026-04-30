# apps/follows/serializers.py

from rest_framework import serializers
from .models import Follow
from django.conf import settings


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()
    follower_id = serializers.IntegerField(source='follower.id', read_only=True)
    following_id = serializers.IntegerField(source='following.id', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_id', 'following', 'following_id', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']