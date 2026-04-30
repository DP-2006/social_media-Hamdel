# apps/stories/serializers.py

from rest_framework import serializers
from .models import Story, StoryView


class StorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    views_count = serializers.SerializerMethodField()
    is_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'user', 'image', 'caption', 'views_count', 'is_viewed', 'created_at', 'expires_at']
        read_only_fields = ['id', 'user', 'created_at', 'expires_at']

    def get_views_count(self, obj):
        return obj.views.count()

    def get_is_viewed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.views.filter(viewer=request.user).exists()
        return False


class StoryViewSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField()

    class Meta:
        model = StoryView
        fields = ['id', 'viewer', 'created_at']
        read_only_fields = ['id', 'viewer', 'created_at']