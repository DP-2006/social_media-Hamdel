

# apps/stories/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Story, StoryView

User = get_user_model()


class StoryUserMinimalSerializer(serializers.ModelSerializer):
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


class StorySerializer(serializers.ModelSerializer):
    user = StoryUserMinimalSerializer(read_only=True)
    views_count = serializers.SerializerMethodField()
    is_viewed = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    remaining_hours = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    media_url = serializers.SerializerMethodField()
    media_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = [
            'id', 'user', 'image', 'image_url', 'video', 'video_url',
            'media_url', 'media_type', 'caption', 
            'views_count', 'is_viewed', 'is_expired', 'remaining_hours',
            'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'expires_at']
    
    def get_views_count(self, obj):
        return obj.views.count()
    
    def get_is_viewed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.views.filter(viewer=request.user).exists()
        return False
    
    def get_is_expired(self, obj):
        return obj.expires_at <= timezone.now()
    
    def get_remaining_hours(self, obj):
        if obj.expires_at > timezone.now():
            delta = obj.expires_at - timezone.now()
            return round(delta.total_seconds() / 3600, 1)
        return 0
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None
    
    def get_video_url(self, obj):
        if obj.video and hasattr(obj.video, 'url'):
            return obj.video.url
        return None
    
    def get_media_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        if obj.video and hasattr(obj.video, 'url'):
            return obj.video.url
        return None
    
    def get_media_type(self, obj):
        if obj.image:
            return 'image'
        if obj.video:
            return 'video'
        return None


class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['image', 'video', 'caption']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'video': {'required': False, 'allow_null': True},
            'caption': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, data):
        if not data.get('image') and not data.get('video'):
            raise serializers.ValidationError("Either image or video is required for story")
        return data
    
    def validate_caption(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Caption cannot exceed 500 characters")
        return value
    
    def validate_video(self, value):
        if value:
            if value.size > 20 * 1024 * 1024:
                raise serializers.ValidationError("Video file size cannot exceed 20 MB")
            allowed_types = ['video/mp4', 'video/quicktime', 'video/x-msvideo']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only MP4, MOV, and AVI video formats are supported")
        return value
    
    def validate_image(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 10 MB")
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, GIF, and WEBP image formats are supported")
        return value


class StoryViewSerializer(serializers.ModelSerializer):
    viewer = StoryUserMinimalSerializer(read_only=True)
    viewer_id = serializers.IntegerField(write_only=True, required=False)
    viewer_username = serializers.CharField(source='viewer.username', read_only=True)
    
    class Meta:
        model = StoryView
        fields = ['id', 'story', 'viewer', 'viewer_id', 'viewer_username', 'created_at']
        read_only_fields = ['id', 'viewer', 'created_at']


class StoryViewerSerializer(serializers.ModelSerializer):
    viewer = StoryUserMinimalSerializer(read_only=True)
    viewed_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = StoryView
        fields = ['id', 'viewer', 'viewed_at']


class StoryIdSerializer(serializers.Serializer):
    story_id = serializers.IntegerField(required=True)


class StoryViewResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default="viewed")
    success = serializers.BooleanField(default=True)


class StoryListQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False, default=20, min_value=1, max_value=50)
    offset = serializers.IntegerField(required=False, default=0, min_value=0)
    include_expired = serializers.BooleanField(required=False, default=False)


class StoryDeleteResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()


class MyStoriesResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    data = StorySerializer(many=True)
    count = serializers.IntegerField()


class ActiveStoriesResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    count = serializers.IntegerField()
    data = StorySerializer(many=True)


class StoryViewersResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    count = serializers.IntegerField()
    data = StoryViewerSerializer(many=True)


class ErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    error = serializers.CharField()
    detail = serializers.CharField(required=False)