
# apps/messaging/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message, GroupConversation, GroupMessage, GroupMember

User = get_user_model()

class UserMinimalSerializer(serializers.ModelSerializer):
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
        if request and hasattr(obj, 'sender'):
            return obj.sender == request.user
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
            return UserMinimalSerializer(other).data if other else None
        return None
    
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        return MessageSerializer(last, context=self.context).data if last else None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

class StartConversationSerializer(serializers.Serializer):
    target_id = serializers.UUIDField(required=True)


class TargetAnalysisSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class OpeningMessageSuggestionsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    count = serializers.IntegerField(required=False, default=3, min_value=1, max_value=5)


class ReplySuggestionSerializer(serializers.Serializer):
    last_message = serializers.CharField(required=True, max_length=500)


class IceBreakerTopicsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class ConversationIdSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(required=True)

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'role', 'joined_at', 'is_muted']
        read_only_fields = ['id', 'joined_at']


class GroupMessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField()
    is_read_by_me = serializers.SerializerMethodField()
    read_by_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupMessage
        fields = ['id', 'sender', 'content', 'created_at', 'is_read', 'is_mine', 'is_read_by_me', 'read_by_count']
        read_only_fields = ['id', 'created_at', 'is_read']
    
    def get_is_mine(self, obj):
        request = self.context.get('request')
        return request and obj.sender == request.user
    
    def get_is_read_by_me(self, obj):
        request = self.context.get('request')
        if request:
            return obj.read_by.filter(id=request.user.id).exists()
        return False
    
    def get_read_by_count(self, obj):
        return obj.read_by.count()


class GroupConversationSerializer(serializers.ModelSerializer):
    members = UserMinimalSerializer(many=True, read_only=True)
    admin = UserMinimalSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupConversation
        fields = ['id', 'title', 'avatar', 'description', 'members', 'admin',
                  'member_count', 'is_member', 'is_admin', 'last_message',
                  'last_message_at', 'last_message_preview', 'unread_count', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_message_at']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        return request and obj.members.filter(id=request.user.id).exists()
    
    def get_is_admin(self, obj):
        request = self.context.get('request')
        return request and obj.admin == request.user
    
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        return GroupMessageSerializer(last, context=self.context).data if last else None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(read_by=request.user).count()
        return 0


class CreateGroupSerializer(serializers.ModelSerializer):
    member_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    
    class Meta:
        model = GroupConversation
        fields = ['title', 'avatar', 'description', 'member_ids']
    
    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        request = self.context.get('request')
        
        group = GroupConversation.objects.create(
            **validated_data,
            admin=request.user
        )
        
        group.members.add(request.user)
        for member_id in member_ids:
            if member_id != request.user.id:
                group.members.add(member_id)
        
        for member in group.members.all():
            role = 'admin' if member == request.user else 'member'
            GroupMember.objects.create(group=group, user=member, role=role)
        
        return group

class AddMemberToGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=True)


class GroupDetailSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)


class MemberActionSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

class LeaveGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)