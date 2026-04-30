# apps/hashtags/serializers.py

from rest_framework import serializers
from .models import Hashtag, PostHashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'usage_count', 'created_at']
        read_only_fields = ['id', 'usage_count', 'created_at']


class TrendingHashtagSerializer(serializers.ModelSerializer):
    """هشتگ‌های trending"""
    class Meta:
        model = Hashtag
        fields = ['id', 'name', 'usage_count']