# # # apps/messaging/serializers.py
# # from rest_framework import serializers
# # from django.contrib.auth import get_user_model
# # from .models import Conversation, Message, GroupConversation, GroupMessage, GroupMember

# # User = get_user_model()


# # # ========== User Minimal Serializer ==========
# # class UserMinimalSerializer(serializers.ModelSerializer):
# #     """Minimal serializer for User model"""
# #     display_name = serializers.SerializerMethodField()
# #     profile_image = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = User
# #         fields = ['id', 'username', 'display_name', 'profile_image', 'phone']
    
# #     def get_display_name(self, obj):
# #         if hasattr(obj, 'profile') and obj.profile:
# #             return obj.profile.display_name or obj.username
# #         return obj.username
    
# #     def get_profile_image(self, obj):
# #         if hasattr(obj, 'profile') and obj.profile and obj.profile.profile_image:
# #             return obj.profile.profile_image.url
# #         return None


# # # ========== Private Chat Serializers ==========
# # class MessageSerializer(serializers.ModelSerializer):
# #     """Serializer for Message model"""
# #     sender = UserMinimalSerializer(read_only=True)
# #     is_mine = serializers.SerializerMethodField()
# #     time_ago = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = Message
# #         fields = ['id', 'sender', 'content', 'created_at', 'is_read', 'read_at', 'is_mine', 'time_ago']
# #         read_only_fields = ['id', 'created_at', 'read_at']
    
# #     def get_is_mine(self, obj):
# #         request = self.context.get('request')
# #         return request and obj.sender == request.user
    
# #     def get_time_ago(self, obj):
# #         from django.utils.timesince import timesince
# #         return timesince(obj.created_at)


# # class ConversationSerializer(serializers.ModelSerializer):
# #     """Serializer for Conversation model"""
# #     participants = UserMinimalSerializer(many=True, read_only=True)
# #     other_participant = serializers.SerializerMethodField()
# #     last_message = serializers.SerializerMethodField()
# #     unread_count = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = Conversation
# #         fields = [
# #             'id', 'participants', 'other_participant', 'last_message',
# #             'last_message_at', 'unread_count', 'created_at'
# #         ]
# #         read_only_fields = ['id', 'created_at', 'last_message_at']
    
# #     def get_other_participant(self, obj):
# #         request = self.context.get('request')
# #         if request:
# #             other = obj.participants.exclude(id=request.user.id).first()
# #             return UserMinimalSerializer(other).data if other else None
# #         return None
    
# #     def get_last_message(self, obj):
# #         last = obj.messages.order_by('-created_at').first()
# #         return MessageSerializer(last, context=self.context).data if last else None
    
# #     def get_unread_count(self, obj):
# #         request = self.context.get('request')
# #         if request:
# #             return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
# #         return 0


# # # ========== Group Chat Serializers ==========
# # class GroupMemberSerializer(serializers.ModelSerializer):
# #     """Serializer for GroupMember model"""
# #     user = UserMinimalSerializer(read_only=True)
# #     user_id = serializers.IntegerField(write_only=True, required=False)
# #     role_display = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = GroupMember
# #         fields = ['id', 'user', 'user_id', 'role', 'role_display', 'joined_at', 'is_muted']
# #         read_only_fields = ['id', 'joined_at']
    
# #     def get_role_display(self, obj):
# #         roles = {
# #             'admin': 'مدیر',
# #             'moderator': 'مدیر انجمن',
# #             'member': 'عضو عادی'
# #         }
# #         return roles.get(obj.role, obj.role)


# # class GroupMessageSerializer(serializers.ModelSerializer):
# #     """Serializer for GroupMessage model"""
# #     sender = UserMinimalSerializer(read_only=True)
# #     is_mine = serializers.SerializerMethodField()
# #     is_read_by_me = serializers.SerializerMethodField()
# #     read_by_count = serializers.SerializerMethodField()
# #     read_by_users = serializers.SerializerMethodField()
# #     time_ago = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = GroupMessage
# #         fields = [
# #             'id', 'sender', 'content', 'created_at', 'is_read',
# #             'is_mine', 'is_read_by_me', 'read_by_count', 'read_by_users', 'time_ago'
# #         ]
# #         read_only_fields = ['id', 'created_at']
    
# #     def get_is_mine(self, obj):
# #         request = self.context.get('request')
# #         return request and obj.sender == request.user
    
# #     def get_is_read_by_me(self, obj):
# #         request = self.context.get('request')
# #         if request:
# #             return obj.read_by.filter(id=request.user.id).exists()
# #         return False
    
# #     def get_read_by_count(self, obj):
# #         return obj.read_by.count()
    
# #     def get_read_by_users(self, obj):
# #         return UserMinimalSerializer(obj.read_by.all(), many=True).data
    
# #     def get_time_ago(self, obj):
# #         from django.utils.timesince import timesince
# #         return timesince(obj.created_at)


# # class GroupConversationSerializer(serializers.ModelSerializer):
# #     """Serializer for GroupConversation model"""
# #     members = UserMinimalSerializer(many=True, read_only=True)
# #     admin = UserMinimalSerializer(read_only=True)
# #     member_count = serializers.SerializerMethodField()
# #     is_member = serializers.SerializerMethodField()
# #     is_admin = serializers.SerializerMethodField()
# #     last_message = serializers.SerializerMethodField()
# #     unread_count = serializers.SerializerMethodField()
# #     my_role = serializers.SerializerMethodField()
    
# #     class Meta:
# #         model = GroupConversation
# #         fields = [
# #             'id', 'title', 'avatar', 'description', 'members', 'admin',
# #             'member_count', 'is_member', 'is_admin', 'my_role', 'last_message',
# #             'last_message_at', 'last_message_preview', 'unread_count', 'is_active',
# #             'created_at'
# #         ]
# #         read_only_fields = ['id', 'created_at', 'last_message_at']
    
# #     def get_member_count(self, obj):
# #         return obj.members.count()
    
# #     def get_is_member(self, obj):
# #         request = self.context.get('request')
# #         return request and obj.members.filter(id=request.user.id).exists()
    
# #     def get_is_admin(self, obj):
# #         request = self.context.get('request')
# #         return request and obj.admin == request.user
    
# #     def get_my_role(self, obj):
# #         request = self.context.get('request')
# #         if request:
# #             member = GroupMember.objects.filter(group=obj, user=request.user).first()
# #             if member:
# #                 roles = {'admin': 'مدیر', 'moderator': 'مدیر انجمن', 'member': 'عضو عادی'}
# #                 return roles.get(member.role, member.role)
# #         return None
    
# #     def get_last_message(self, obj):
# #         last = obj.messages.order_by('-created_at').first()
# #         return GroupMessageSerializer(last, context=self.context).data if last else None
    
# #     def get_unread_count(self, obj):
# #         request = self.context.get('request')
# #         if request:
# #             return obj.messages.filter(is_read=False).exclude(read_by=request.user).count()
# #         return 0


# # class CreateGroupSerializer(serializers.ModelSerializer):
# #     """Serializer for creating a new group"""
# #     member_ids = serializers.ListField(
# #         child=serializers.IntegerField(),
# #         write_only=True,
# #         required=False,
# #         help_text="List of user IDs to add as members"
# #     )
    
# #     class Meta:
# #         model = GroupConversation
# #         fields = ['title', 'avatar', 'description', 'member_ids']
    
# #     def validate_title(self, value):
# #         if not value or not value.strip():
# #             raise serializers.ValidationError("Group title is required")
# #         if len(value) > 100:
# #             raise serializers.ValidationError("Group title cannot exceed 100 characters")
# #         return value.strip()
    
# #     def create(self, validated_data):
# #         member_ids = validated_data.pop('member_ids', [])
# #         request = self.context.get('request')
        
# #         group = GroupConversation.objects.create(
# #             **validated_data,
# #             admin=request.user
# #         )
        
# #         # Add members
# #         group.members.add(request.user)  # Creator
# #         for member_id in member_ids:
# #             if member_id != request.user.id:
# #                 group.members.add(member_id)
        
# #         # Create GroupMember records
# #         for member in group.members.all():
# #             role = 'admin' if member == request.user else 'member'
# #             GroupMember.objects.create(group=group, user=member, role=role)
        
# #         return group


# # class AddMemberToGroupSerializer(serializers.Serializer):
# #     """Serializer for adding members to a group"""
# #     user_ids = serializers.ListField(
# #         child=serializers.IntegerField(),
# #         required=True,
# #         help_text="List of user IDs to add to the group"
# #     )
# #     group_id = serializers.IntegerField(
# #         required=False,
# #         write_only=True,
# #         help_text="ID of the group (can be passed in URL)"
# #     )
    
# #     def validate_user_ids(self, value):
# #         if not value:
# #             raise serializers.ValidationError("At least one user ID is required")
# #         if len(value) > 50:
# #             raise serializers.ValidationError("Cannot add more than 50 users at once")
# #         return value


# # # ========== Request/Response Serializers ==========
# # class StartConversationSerializer(serializers.Serializer):
# #     """Serializer for starting a conversation"""
# #     target_id = serializers.IntegerField(
# #         required=True,
# #         help_text="ID of the user to start conversation with"
# #     )


# # class TargetAnalysisSerializer(serializers.Serializer):
# #     """Serializer for target user analysis"""
# #     user_id = serializers.IntegerField(
# #         required=True,
# #         help_text="ID of the user to analyze"
# #     )


# # class OpeningMessageSuggestionsSerializer(serializers.Serializer):
# #     """Serializer for opening message suggestions"""
# #     user_id = serializers.IntegerField(
# #         required=True,
# #         help_text="ID of the target user"
# #     )
# #     count = serializers.IntegerField(
# #         required=False,
# #         default=3,
# #         min_value=1,
# #         max_value=5,
# #         help_text="Number of suggestions to return"
# #     )


# # class ReplySuggestionSerializer(serializers.Serializer):
# #     """Serializer for reply suggestions"""
# #     last_message = serializers.CharField(
# #         required=True,
# #         max_length=500,
# #         help_text="Last message content"
# #     )


# # class IceBreakerTopicsSerializer(serializers.Serializer):
# #     """Serializer for icebreaker topics"""
# #     user_id = serializers.IntegerField(
# #         required=True,
# #         help_text="ID of the target user"
# #     )


# # class ConversationIdSerializer(serializers.Serializer):
# #     """Serializer for conversation ID validation"""
# #     conversation_id = serializers.IntegerField(required=True)


# # class GroupDetailSerializer(serializers.Serializer):
# #     """Serializer for group detail operations"""
# #     group_id = serializers.IntegerField(
# #         required=True,
# #         help_text="ID of the group"
# #     )


# # class MemberActionSerializer(serializers.Serializer):
# #     """Serializer for member actions (add/remove)"""
# #     group_id = serializers.IntegerField(required=True)
# #     user_id = serializers.IntegerField(required=True)


# # class LeaveGroupSerializer(serializers.Serializer):
# #     """Serializer for leaving a group"""
# #     group_id = serializers.IntegerField(required=True)


# # class MarkReadSerializer(serializers.Serializer):
# #     """Serializer for marking messages as read"""
# #     message_ids = serializers.ListField(
# #         child=serializers.IntegerField(),
# #         required=False,
# #         help_text="List of message IDs to mark as read"
# #     )
# #     mark_all = serializers.BooleanField(
# #         required=False,
# #         default=False,
# #         help_text="Mark all messages as read"
# #     )






# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Conversation, Message, GroupConversation, GroupMessage, GroupMember

# User = get_user_model()


# class UserMinimalSerializer(serializers.ModelSerializer):
#     """Minimal serializer for User model"""
#     display_name = serializers.SerializerMethodField()
#     profile_image = serializers.SerializerMethodField()
    
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'display_name', 'profile_image', 'phone']
    
#     def get_display_name(self, obj) -> str:
#         if hasattr(obj, 'profile') and obj.profile:
#             return obj.profile.display_name or obj.username
#         return obj.username
    
#     def get_profile_image(self, obj) -> str | None:
#         if hasattr(obj, 'profile') and obj.profile and obj.profile.profile_image:
#             return obj.profile.profile_image.url
#         return None


# class MessageSerializer(serializers.ModelSerializer):
#     """Serializer for Message model"""
#     sender = UserMinimalSerializer(read_only=True)
#     is_mine = serializers.SerializerMethodField()
#     time_ago = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Message
#         fields = ['id', 'sender', 'content', 'created_at', 'is_read', 'read_at', 'is_mine', 'time_ago']
#         read_only_fields = ['id', 'created_at', 'read_at']
    
#     def get_is_mine(self, obj) -> bool:
#         request = self.context.get('request')
#         return request and obj.sender == request.user
    
#     def get_time_ago(self, obj) -> str:
#         from django.utils.timesince import timesince
#         return timesince(obj.created_at)


# class ConversationSerializer(serializers.ModelSerializer):
#     """Serializer for Conversation model"""
#     participants = UserMinimalSerializer(many=True, read_only=True)
#     other_participant = serializers.SerializerMethodField()
#     last_message = serializers.SerializerMethodField()
#     unread_count = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Conversation
#         fields = [
#             'id', 'participants', 'other_participant', 'last_message',
#             'last_message_at', 'unread_count', 'created_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'last_message_at']
    
#     def get_other_participant(self, obj) -> dict | None:
#         request = self.context.get('request')
#         if request:
#             other = obj.participants.exclude(id=request.user.id).first()
#             return UserMinimalSerializer(other).data if other else None
#         return None
    
#     def get_last_message(self, obj) -> dict | None:
#         last = obj.messages.order_by('-created_at').first()
#         return MessageSerializer(last, context=self.context).data if last else None
    
#     def get_unread_count(self, obj) -> int:
#         request = self.context.get('request')
#         if request:
#             return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
#         return 0


# class GroupMemberSerializer(serializers.ModelSerializer):
#     """Serializer for GroupMember model"""
#     user = UserMinimalSerializer(read_only=True)
#     user_id = serializers.IntegerField(write_only=True, required=False)
#     role_display = serializers.SerializerMethodField()
    
#     class Meta:
#         model = GroupMember
#         fields = ['id', 'user', 'user_id', 'role', 'role_display', 'joined_at', 'is_muted']
#         read_only_fields = ['id', 'joined_at']
    
#     def get_role_display(self, obj) -> str:
#         roles = {
#             'admin': 'مدیر',
#             'moderator': 'مدیر انجمن',
#             'member': 'عضو عادی'
#         }
#         return roles.get(obj.role, obj.role)


# class GroupMessageSerializer(serializers.ModelSerializer):
#     """Serializer for GroupMessage model"""
#     sender = UserMinimalSerializer(read_only=True)
#     is_mine = serializers.SerializerMethodField()
#     is_read_by_me = serializers.SerializerMethodField()
#     read_by_count = serializers.SerializerMethodField()
#     read_by_users = serializers.SerializerMethodField()
#     time_ago = serializers.SerializerMethodField()
    
#     class Meta:
#         model = GroupMessage
#         fields = [
#             'id', 'sender', 'content', 'created_at', 'is_read',
#             'is_mine', 'is_read_by_me', 'read_by_count', 'read_by_users', 'time_ago'
#         ]
#         read_only_fields = ['id', 'created_at']
    
#     def get_is_mine(self, obj) -> bool:
#         request = self.context.get('request')
#         return request and obj.sender == request.user
    
#     def get_is_read_by_me(self, obj) -> bool:
#         request = self.context.get('request')
#         if request:
#             return obj.read_by.filter(id=request.user.id).exists()
#         return False
    
#     def get_read_by_count(self, obj) -> int:
#         return obj.read_by.count()
    
#     def get_read_by_users(self, obj) -> list:
#         return UserMinimalSerializer(obj.read_by.all(), many=True).data
    
#     def get_time_ago(self, obj) -> str:
#         from django.utils.timesince import timesince
#         return timesince(obj.created_at)


# class GroupConversationSerializer(serializers.ModelSerializer):
#     """Serializer for GroupConversation model"""
#     members = UserMinimalSerializer(many=True, read_only=True)
#     admin = UserMinimalSerializer(read_only=True)
#     member_count = serializers.SerializerMethodField()
#     is_member = serializers.SerializerMethodField()
#     is_admin = serializers.SerializerMethodField()
#     last_message = serializers.SerializerMethodField()
#     unread_count = serializers.SerializerMethodField()
#     my_role = serializers.SerializerMethodField()
    
#     class Meta:
#         model = GroupConversation
#         fields = [
#             'id', 'title', 'avatar', 'description', 'members', 'admin',
#             'member_count', 'is_member', 'is_admin', 'my_role', 'last_message',
#             'last_message_at', 'last_message_preview', 'unread_count', 'is_active',
#             'created_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'last_message_at']
    
#     def get_member_count(self, obj) -> int:
#         return obj.members.count()
    
#     def get_is_member(self, obj) -> bool:
#         request = self.context.get('request')
#         return request and obj.members.filter(id=request.user.id).exists()
    
#     def get_is_admin(self, obj) -> bool:
#         request = self.context.get('request')
#         return request and obj.admin == request.user
    
#     def get_my_role(self, obj) -> str | None:
#         request = self.context.get('request')
#         if request:
#             member = GroupMember.objects.filter(group=obj, user=request.user).first()
#             if member:
#                 roles = {'admin': 'مدیر', 'moderator': 'مدیر انجمن', 'member': 'عضو عادی'}
#                 return roles.get(member.role, member.role)
#         return None
    
#     def get_last_message(self, obj) -> dict | None:
#         last = obj.messages.order_by('-created_at').first()
#         return GroupMessageSerializer(last, context=self.context).data if last else None
    
#     def get_unread_count(self, obj) -> int:
#         request = self.context.get('request')
#         if request:
#             return obj.messages.filter(is_read=False).exclude(read_by=request.user).count()
#         return 0


# class CreateGroupSerializer(serializers.ModelSerializer):
#     """Serializer for creating a new group"""
#     member_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True,
#         required=False,
#         help_text="List of user IDs to add as members"
#     )
    
#     class Meta:
#         model = GroupConversation
#         fields = ['title', 'avatar', 'description', 'member_ids']
    
#     def validate_title(self, value) -> str:
#         if not value or not value.strip():
#             raise serializers.ValidationError("Group title is required")
#         if len(value) > 100:
#             raise serializers.ValidationError("Group title cannot exceed 100 characters")
#         return value.strip()
    
#     def create(self, validated_data):
#         member_ids = validated_data.pop('member_ids', [])
#         request = self.context.get('request')
        
#         group = GroupConversation.objects.create(
#             **validated_data,
#             admin=request.user
#         )
        
#         # Add members
#         group.members.add(request.user)  # Creator
#         for member_id in member_ids:
#             if member_id != request.user.id:
#                 group.members.add(member_id)
        
#         # Create GroupMember records
#         for member in group.members.all():
#             role = 'admin' if member == request.user else 'member'
#             GroupMember.objects.create(group=group, user=member, role=role)
        
#         return group


# class AddMemberToGroupSerializer(serializers.Serializer):
#     """Serializer for adding members to a group"""
#     user_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         required=True,
#         help_text="List of user IDs to add to the group"
#     )
#     group_id = serializers.IntegerField(
#         required=False,
#         write_only=True,
#         help_text="ID of the group (can be passed in URL)"
#     )
    
#     def validate_user_ids(self, value) -> list:
#         if not value:
#             raise serializers.ValidationError("At least one user ID is required")
#         if len(value) > 50:
#             raise serializers.ValidationError("Cannot add more than 50 users at once")
#         return value


# class StartConversationSerializer(serializers.Serializer):
#     """Serializer for starting a conversation"""
#     target_id = serializers.IntegerField(
#         required=True,
#         help_text="ID of the user to start conversation with"
#     )


# class TargetAnalysisSerializer(serializers.Serializer):
#     """Serializer for target user analysis"""
#     user_id = serializers.IntegerField(
#         required=True,
#         help_text="ID of the user to analyze"
#     )


# class OpeningMessageSuggestionsSerializer(serializers.Serializer):
#     """Serializer for opening message suggestions"""
#     user_id = serializers.IntegerField(
#         required=True,
#         help_text="ID of the target user"
#     )
#     count = serializers.IntegerField(
#         required=False,
#         default=3,
#         min_value=1,
#         max_value=5,
#         help_text="Number of suggestions to return"
#     )


# class ReplySuggestionSerializer(serializers.Serializer):
#     """Serializer for reply suggestions"""
#     last_message = serializers.CharField(
#         required=True,
#         max_length=500,
#         help_text="Last message content"
#     )


# class IceBreakerTopicsSerializer(serializers.Serializer):
#     """Serializer for icebreaker topics"""
#     user_id = serializers.IntegerField(
#         required=True,
#         help_text="ID of the target user"
#     )


# class ConversationIdSerializer(serializers.Serializer):
#     """Serializer for conversation ID validation"""
#     conversation_id = serializers.IntegerField(required=True)


# class GroupDetailSerializer(serializers.Serializer):
#     """Serializer for group detail operations"""
#     group_id = serializers.IntegerField(
#         required=True,
#         help_text="ID of the group"
#     )


# class MemberActionSerializer(serializers.Serializer):
#     """Serializer for member actions (add/remove)"""
#     group_id = serializers.IntegerField(required=True)
#     user_id = serializers.IntegerField(required=True)


# class LeaveGroupSerializer(serializers.Serializer):
#     """Serializer for leaving a group"""
#     group_id = serializers.IntegerField(required=True)


# class MarkReadSerializer(serializers.Serializer):
#     """Serializer for marking messages as read"""
#     message_ids = serializers.ListField(
#         child=serializers.IntegerField(),      
#         required=False,
#         help_text="List of message IDs to mark as read"
#     )
#     mark_all = serializers.BooleanField(
#         required=False,
#         default=False,
#         help_text="Mark all messages as read"
#     )












"""
Serializers for messaging app
Compatible with DRF, Swagger, and AI-powered views
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from typing import Dict, Any, List, Optional
from .models import Conversation, Message, GroupConversation, GroupMessage, GroupMember

User = get_user_model()


# ========== User Minimal Serializer ==========
class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for User model with display name and profile image"""
    
    display_name = serializers.SerializerMethodField(
        help_text="User's display name (from profile or username)"
    )
    profile_image = serializers.SerializerMethodField(
        help_text="URL of user's profile image"
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'profile_image', 'phone']
        help_text = {
            'id': 'Unique user identifier',
            'username': 'Unique username',
            'phone': 'Phone number (if available)',
        }
    
    def get_display_name(self, obj: User) -> str:
        """Get user's display name"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.display_name or obj.username
        return obj.username
    
    def get_profile_image(self, obj: User) -> Optional[str]:
        """Get user's profile image URL"""
        if hasattr(obj, 'profile') and obj.profile and obj.profile.profile_image:
            return obj.profile.profile_image.url
        return None


# ========== Private Chat Serializers ==========
class MessageSerializer(serializers.ModelSerializer):
    """Serializer for private messages"""
    
    sender = UserMinimalSerializer(read_only=True, help_text="Message sender information")
    is_mine = serializers.SerializerMethodField(help_text="Whether the message belongs to current user")
    time_ago = serializers.SerializerMethodField(help_text="Human-readable time since message sent")
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'content', 'created_at', 'is_read', 
            'read_at', 'is_mine', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
    
    def get_is_mine(self, obj: Message) -> bool:
        """Check if message is sent by current user"""
        request = self.context.get('request')
        return request and obj.sender == request.user
    
    def get_time_ago(self, obj: Message) -> str:
        """Get human-readable time since message creation"""
        from django.utils.timesince import timesince
        return timesince(obj.created_at)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for private conversations"""
    
    participants = UserMinimalSerializer(many=True, read_only=True, help_text="All participants in conversation")
    other_participant = serializers.SerializerMethodField(help_text="The other participant (not current user)")
    last_message = serializers.SerializerMethodField(help_text="Most recent message in conversation")
    unread_count = serializers.SerializerMethodField(help_text="Number of unread messages")
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'other_participant', 'last_message',
            'last_message_at', 'unread_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'last_message_at']
    
    def get_other_participant(self, obj: Conversation) -> Optional[Dict]:
        """Get the other participant in conversation"""
        request = self.context.get('request')
        if request:
            other = obj.participants.exclude(id=request.user.id).first()
            return UserMinimalSerializer(other).data if other else None
        return None
    
    def get_last_message(self, obj: Conversation) -> Optional[Dict]:
        """Get the last message in conversation"""
        last = obj.messages.order_by('-created_at').first()
        return MessageSerializer(last, context=self.context).data if last else None
    
    def get_unread_count(self, obj: Conversation) -> int:
        """Count unread messages for current user"""
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


# ========== Group Chat Serializers ==========
class GroupMemberSerializer(serializers.ModelSerializer):
    """Serializer for group members"""
    
    user = UserMinimalSerializer(read_only=True, help_text="Member user information")
    user_id = serializers.IntegerField(write_only=True, required=False, help_text="User ID for adding members")
    role_display = serializers.SerializerMethodField(help_text="Human-readable role name")
    
    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'user_id', 'role', 'role_display', 'joined_at', 'is_muted']
        read_only_fields = ['id', 'joined_at']
    
    def get_role_display(self, obj: GroupMember) -> str:
        """Get Persian role name"""
        roles = {
            'admin': 'مدیر',
            'moderator': 'مدیر انجمن',
            'member': 'عضو عادی'
        }
        return roles.get(obj.role, obj.role)


class GroupMessageSerializer(serializers.ModelSerializer):
    """Serializer for group messages"""
    
    sender = UserMinimalSerializer(read_only=True, help_text="Message sender")
    is_mine = serializers.SerializerMethodField(help_text="Whether message belongs to current user")
    is_read_by_me = serializers.SerializerMethodField(help_text="Whether current user has read this message")
    read_by_count = serializers.SerializerMethodField(help_text="Number of members who read this message")
    read_by_users = serializers.SerializerMethodField(help_text="List of users who read this message")
    time_ago = serializers.SerializerMethodField(help_text="Human-readable time since message sent")
    
    class Meta:
        model = GroupMessage
        fields = [
            'id', 'sender', 'content', 'created_at', 'is_read',
            'is_mine', 'is_read_by_me', 'read_by_count', 'read_by_users', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_mine(self, obj: GroupMessage) -> bool:
        """Check if message is sent by current user"""
        request = self.context.get('request')
        return request and obj.sender == request.user
    
    def get_is_read_by_me(self, obj: GroupMessage) -> bool:
        """Check if current user has read this message"""
        request = self.context.get('request')
        if request:
            return obj.read_by.filter(id=request.user.id).exists()
        return False
    
    def get_read_by_count(self, obj: GroupMessage) -> int:
        """Get number of members who read this message"""
        return obj.read_by.count()
    
    def get_read_by_users(self, obj: GroupMessage) -> List[Dict]:
        """Get list of users who read this message"""
        return UserMinimalSerializer(obj.read_by.all(), many=True).data
    
    def get_time_ago(self, obj: GroupMessage) -> str:
        """Get human-readable time since message creation"""
        from django.utils.timesince import timesince
        return timesince(obj.created_at)


class GroupConversationSerializer(serializers.ModelSerializer):
    """Serializer for group conversations"""
    
    members = UserMinimalSerializer(many=True, read_only=True, help_text="Group members")
    admin = UserMinimalSerializer(read_only=True, help_text="Group admin")
    member_count = serializers.SerializerMethodField(help_text="Total number of members")
    is_member = serializers.SerializerMethodField(help_text="Whether current user is a member")
    is_admin = serializers.SerializerMethodField(help_text="Whether current user is admin")
    last_message = serializers.SerializerMethodField(help_text="Most recent message")
    unread_count = serializers.SerializerMethodField(help_text="Number of unread messages for current user")
    my_role = serializers.SerializerMethodField(help_text="Current user's role in group")
    
    class Meta:
        model = GroupConversation
        fields = [
            'id', 'title', 'avatar', 'description', 'members', 'admin',
            'member_count', 'is_member', 'is_admin', 'my_role', 'last_message',
            'last_message_at', 'last_message_preview', 'unread_count', 'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'last_message_at']
    
    def get_member_count(self, obj: GroupConversation) -> int:
        """Get member count"""
        return obj.members.count()
    
    def get_is_member(self, obj: GroupConversation) -> bool:
        """Check if current user is member"""
        request = self.context.get('request')
        return request and obj.members.filter(id=request.user.id).exists()
    
    def get_is_admin(self, obj: GroupConversation) -> bool:
        """Check if current user is admin"""
        request = self.context.get('request')
        return request and obj.admin == request.user
    
    def get_my_role(self, obj: GroupConversation) -> Optional[str]:
        """Get current user's role in Persian"""
        request = self.context.get('request')
        if request:
            member = GroupMember.objects.filter(group=obj, user=request.user).first()
            if member:
                roles = {'admin': 'مدیر', 'moderator': 'مدیر انجمن', 'member': 'عضو عادی'}
                return roles.get(member.role, member.role)
        return None
    
    def get_last_message(self, obj: GroupConversation) -> Optional[Dict]:
        """Get last message in group"""
        last = obj.messages.order_by('-created_at').first()
        return GroupMessageSerializer(last, context=self.context).data if last else None
    
    def get_unread_count(self, obj: GroupConversation) -> int:
        """Count unread messages for current user"""
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(read_by=request.user).count()
        return 0


class CreateGroupSerializer(serializers.ModelSerializer):
    """Serializer for creating a new group"""
    
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of user IDs to add as members (excluding creator)"
    )
    
    class Meta:
        model = GroupConversation
        fields = ['title', 'avatar', 'description', 'member_ids']
    
    def validate_title(self, value: str) -> str:
        """Validate group title"""
        if not value or not value.strip():
            raise serializers.ValidationError("عنوان گروه الزامی است")
        if len(value) > 100:
            raise serializers.ValidationError("عنوان گروه نمی‌تواند بیشتر از ۱۰۰ کاراکتر باشد")
        return value.strip()
    
    def create(self, validated_data: Dict) -> GroupConversation:
        """Create group with members"""
        member_ids = validated_data.pop('member_ids', [])
        request = self.context.get('request')
        
        group = GroupConversation.objects.create(
            **validated_data,
            admin=request.user
        )
        
        # Add members
        group.members.add(request.user)  # Creator automatically added
        for member_id in member_ids:
            if member_id != request.user.id:
                group.members.add(member_id)
        
        # Create GroupMember records
        for member in group.members.all():
            role = 'admin' if member == request.user else 'member'
            GroupMember.objects.create(group=group, user=member, role=role)
        
        return group


class AddMemberToGroupSerializer(serializers.Serializer):
    """Serializer for adding members to a group"""
    
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="لیست شناسه کاربرانی که باید به گروه اضافه شوند"
    )
    group_id = serializers.IntegerField(
        required=False,
        write_only=True,
        help_text="شناسه گروه (می‌تواند در URL ارسال شود)"
    )
    
    def validate_user_ids(self, value: List[int]) -> List[int]:
        """Validate user IDs list"""
        if not value:
            raise serializers.ValidationError("حداقل یک کاربر باید انتخاب شود")
        if len(value) > 50:
            raise serializers.ValidationError("نمی‌توان بیش از ۵۰ کاربر را یکباره اضافه کرد")
        return value


# ========== AI-Powered Serializers ==========
class StartConversationSerializer(serializers.Serializer):
    """Serializer for starting a new conversation"""
    
    target_id = serializers.IntegerField(
        required=True,
        help_text="شناسه کاربری که می‌خواهید با او مکالمه را شروع کنید"
    )
    
    def validate_target_id(self, value: int) -> int:
        """Validate target user exists"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("کاربر مورد نظر یافت نشد")
        return value


class TargetAnalysisSerializer(serializers.Serializer):
    """Serializer for AI-powered target user personality analysis"""
    
    user_id = serializers.IntegerField(
        required=True,
        help_text="شناسه کاربر هدف برای تحلیل شخصیت"
    )
    
    def validate_user_id(self, value: int) -> int:
        """Validate user exists"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("کاربر مورد نظر یافت نشد")
        return value


class OpeningMessageSuggestionsSerializer(serializers.Serializer):
    """Serializer for AI-powered opening message suggestions"""
    
    user_id = serializers.IntegerField(
        required=True,
        help_text="شناسه کاربر هدف برای پیشنهاد پیام اولیه"
    )
    count = serializers.IntegerField(
        required=False,
        default=3,
        min_value=1,
        max_value=5,
        help_text="تعداد پیشنهادات مورد نیاز (۱ تا ۵)"
    )
    
    def validate_user_id(self, value: int) -> int:
        """Validate user exists"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("کاربر مورد نظر یافت نشد")
        return value


class ReplySuggestionSerializer(serializers.Serializer):
    """Serializer for AI-powered reply suggestions"""
    
    last_message = serializers.CharField(
        required=True,
        max_length=500,
        help_text="متن آخرین پیام دریافتی برای پیشنهاد پاسخ"
    )
    context = serializers.CharField(
        required=False,
        max_length=1000,
        allow_blank=True,
        help_text="متن قبلی مکالمه (اختیاری) برای پاسخ هوشمندتر"
    )
    style = serializers.ChoiceField(
        choices=['friendly', 'professional', 'humorous'],
        default='friendly',
        required=False,
        help_text="سبک پاسخ: دوستانه، رسمی، یا با شوخ‌طبعی"
    )
    
    def validate_last_message(self, value: str) -> str:
        """Validate last message is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("متن آخرین پیام نمی‌تواند خالی باشد")
        return value.strip()


class IceBreakerTopicsSerializer(serializers.Serializer):
    """Serializer for AI-powered icebreaker topics"""
    
    user_id = serializers.IntegerField(
        required=True,
        help_text="شناسه کاربر هدف برای پیشنهاد موضوعات شروع مکالمه"
    )
    
    def validate_user_id(self, value: int) -> int:
        """Validate user exists"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("کاربر مورد نظر یافت نشد")
        return value


# ========== Utility Serializers ==========
class ConversationIdSerializer(serializers.Serializer):
    """Serializer for conversation ID validation"""
    
    conversation_id = serializers.IntegerField(
        required=True,
        help_text="شناسه مکالمه"
    )
    
    def validate_conversation_id(self, value: int) -> int:
        """Validate conversation exists"""
        if not Conversation.objects.filter(id=value).exists():
            raise serializers.ValidationError("مکالمه مورد نظر یافت نشد")
        return value


class GroupDetailSerializer(serializers.Serializer):
    """Serializer for group detail operations"""
    
    group_id = serializers.IntegerField(
        required=True,
        help_text="شناسه گروه"
    )
    
    def validate_group_id(self, value: int) -> int:
        """Validate group exists"""
        if not GroupConversation.objects.filter(id=value).exists():
            raise serializers.ValidationError("گروه مورد نظر یافت نشد")
        return value


class MemberActionSerializer(serializers.Serializer):
    """Serializer for member actions (add/remove)"""
    
    group_id = serializers.IntegerField(
        required=True,
        help_text="شناسه گروه"
    )
    user_id = serializers.IntegerField(
        required=True,
        help_text="شناسه کاربر"
    )
    
    def validate_group_id(self, value: int) -> int:
        """Validate group exists"""
        if not GroupConversation.objects.filter(id=value).exists():
            raise serializers.ValidationError("گروه مورد نظر یافت نشد")
        return value
    
    def validate_user_id(self, value: int) -> int:
        """Validate user exists"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("کاربر مورد نظر یافت نشد")
        return value


class LeaveGroupSerializer(serializers.Serializer):
    """Serializer for leaving a group"""
    
    group_id = serializers.IntegerField(
        required=True,
        help_text="شناسه گروهی که می‌خواهید از آن خارج شوید"
    )
    
    def validate_group_id(self, value: int) -> int:
        """Validate group exists"""
        if not GroupConversation.objects.filter(id=value).exists():
            raise serializers.ValidationError("گروه مورد نظر یافت نشد")
        return value


class MarkReadSerializer(serializers.Serializer):
    """Serializer for marking messages as read"""
    
    message_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="لیست شناسه پیام‌هایی که باید به عنوان خوانده شده علامت بخورند"
    )
    mark_all = serializers.BooleanField(
        required=False,
        default=False,
        help_text="اگر true باشد، همه پیام‌ها به عنوان خوانده شده علامت می‌خورند"
    )
    
    def validate_message_ids(self, value: List[int]) -> List[int]:
        """Validate message IDs if provided"""
        if value and len(value) > 100:
            raise serializers.ValidationError("نمی‌توان بیش از ۱۰۰ پیام را یکباره آپدیت کرد")
        return value


# ========== AI Response Serializers (برای مستندسازی Swagger) ==========
class AIAnalysisResponseSerializer(serializers.Serializer):
    """Serializer for AI analysis response structure"""
    
    personality_type = serializers.CharField(help_text="نوع شخصیت کاربر")
    interests = serializers.ListField(child=serializers.CharField(), help_text="لیست علاقه‌مندی‌ها")
    communication_style = serializers.CharField(help_text="سبک ارتباطی پیشنهادی")
    icebreakers = serializers.ListField(child=serializers.CharField(), help_text="پیشنهادات شروع مکالمه")
    topics_to_avoid = serializers.ListField(child=serializers.CharField(), help_text="موضوعاتی که باید اجتناب شود")
    best_time_to_message = serializers.CharField(help_text="بهترین زمان برای ارسال پیام")
    tips = serializers.ListField(child=serializers.CharField(), help_text="نکات کاربردی برای ارتباط")


class AIOpeningSuggestionsResponseSerializer(serializers.Serializer):
    """Serializer for AI opening suggestions response"""
    
    target = serializers.CharField(help_text="نام کاربر هدف")
    suggestions = serializers.ListField(child=serializers.CharField(), help_text="لیست پیشنهادات پیام اولیه")


class AIReplySuggestionResponseSerializer(serializers.Serializer):
    """Serializer for AI reply suggestion response"""
    
    suggested_reply = serializers.CharField(help_text="پاسخ پیشنهادی اصلی")
    alternatives = serializers.ListField(child=serializers.CharField(), help_text="پاسخ‌های جایگزین")
    source = serializers.ChoiceField(choices=['ai', 'fallback'], help_text="منبع تولید پاسخ")


class AIIcebreakerResponseSerializer(serializers.Serializer):
    """Serializer for AI icebreaker response"""
    
    target = serializers.CharField(help_text="نام کاربر هدف")
    personality = serializers.CharField(help_text="نوع شخصیت")
    topics_to_start = serializers.ListField(child=serializers.CharField(), help_text="موضوعات مناسب برای شروع")
    topics_to_avoid = serializers.ListField(child=serializers.CharField(), help_text="موضوعات نامناسب")
    suggested_questions = serializers.ListField(child=serializers.CharField(), help_text="سوالات پیشنهادی")