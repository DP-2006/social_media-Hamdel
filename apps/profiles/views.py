# apps/profiles/views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Profile
from .serializers import (
    ProfileSerializer, ProfileUpdateSerializer, UserProfileSerializer,
    SearchUserQuerySerializer, UserIdSerializer, FollowToggleResponseSerializer,
    ProfileResponseSerializer, ProfileUpdateResponseSerializer,
    FollowListResponseSerializer, SearchUserResponseSerializer,
    FollowListUserSerializer, SearchUserResultSerializer
)

User = get_user_model()


class ProfileView(GenericAPIView):
    """
    Get, update or partially update user profile
    
    GET: Returns current user's profile
    PUT: Fully updates user's profile
    PATCH: Partially updates user's profile
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer
        return ProfileSerializer
    
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        serializer = ProfileUpdateSerializer(
            profile, 
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            # Return updated profile data
            profile_serializer = ProfileSerializer(profile, context={'request': request})
            return Response({
                "success": True,
                "message": "پروفایل با موفقیت به روز رسانی شد",
                "data": profile_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        serializer = ProfileUpdateSerializer(
            profile, 
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            profile_serializer = ProfileSerializer(profile, context={'request': request})
            return Response({
                "success": True,
                "message": "پروفایل با موفقیت به روز رسانی شد",
                "data": profile_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PublicProfileView(GenericAPIView):
    """
    Get public profile of a user by ID
    
    GET: Returns profile data. Returns 403 if profile is private and user is not following
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserIdSerializer
    
    def get(self, request, user_id):
        # Validate user_id
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        # Check privacy
        if profile.is_private and not request.user == user:
            is_following = profile.followers.filter(id=request.user.id).exists()
            if not is_following:
                return Response({
                    "success": False,
                    "error": "این حساب کاربری خصوصی است"
                }, status=status.HTTP_403_FORBIDDEN)
        
        profile_serializer = ProfileSerializer(profile, context={'request': request})
        return Response({
            "success": True,
            "data": profile_serializer.data
        }, status=status.HTTP_200_OK)


class FollowToggleView(GenericAPIView):
    """
    Toggle follow status for a user
    
    POST: Follow user if not following, unfollow if already following
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserIdSerializer
    
    def post(self, request, user_id):
        # Validate user_id
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        target_user = get_object_or_404(User, id=user_id)
        target_profile = get_object_or_404(Profile, user=target_user)
        
        if request.user == target_user:
            return Response({
                "success": False,
                "error": "نمی‌توانید خودتان را دنبال کنید!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if target_profile.followers.filter(id=request.user.id).exists():
            target_profile.followers.remove(request.user)
            return Response({
                "success": True,
                "action": "unfollowed",
                "message": f"دنبال کردن {target_user.username} لغو شد"
            }, status=status.HTTP_200_OK)
        else:
            target_profile.followers.add(request.user)
            return Response({
                "success": True,
                "action": "followed",
                "message": f"اکنون {target_user.username} را دنبال می‌کنید"
            }, status=status.HTTP_200_OK)


class FollowersListView(GenericAPIView):
    """
    Get list of followers for a user
    
    GET: Returns list of users who follow the specified user
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserIdSerializer
    
    def get(self, request, user_id):
        # Validate user_id
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        followers = profile.followers.select_related('profile').all()
        followers_data = []
        
        for follower in followers:
            follower_profile = Profile.objects.get(user=follower)
            followers_data.append({
                "id": follower.id,
                "username": follower.username,
                "display_name": follower_profile.display_name,
                "avatar": follower_profile.avatar.url if follower_profile.avatar else None,
                "phone": follower.phone
            })
        
        return Response({
            "success": True,
            "count": len(followers_data),
            "data": followers_data
        }, status=status.HTTP_200_OK)


class FollowingListView(GenericAPIView):
    """
    Get list of users that a user is following
    
    GET: Returns list of users followed by the specified user
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserIdSerializer
    
    def get(self, request, user_id):
        # Validate user_id
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        following = profile.following.select_related('profile').all()
        following_data = []
        
        for followed in following:
            followed_profile = Profile.objects.get(user=followed)
            following_data.append({
                "id": followed.id,
                "username": followed.username,
                "display_name": followed_profile.display_name,
                "avatar": followed_profile.avatar.url if followed_profile.avatar else None,
                "phone": followed.phone
            })
        
        return Response({
            "success": True,
            "count": len(following_data),
            "data": following_data
        }, status=status.HTTP_200_OK)


class SearchUserView(GenericAPIView):
    """
    Search for users by username or display name
    
    GET: Returns list of users matching the search query
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchUserQuerySerializer
    
    def get(self, request):
        # Validate query parameters
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = serializer.validated_data.get('q', '')
        limit = serializer.validated_data.get('limit', 20)
        
        # Search in username and display_name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(profile__display_name__icontains=query)
        ).select_related('profile').distinct()[:limit]
        
        results = []
        for user in users:
            profile = Profile.objects.get(user=user)
            is_following = profile.followers.filter(id=request.user.id).exists()
            results.append({
                "id": user.id,
                "username": user.username,
                "display_name": profile.display_name,
                "avatar": profile.avatar.url if profile.avatar else None,
                "is_private": profile.is_private,
                "is_following": is_following
            })
        
        return Response({
            "success": True,
            "count": len(results),
            "data": results
        }, status=status.HTTP_200_OK)


class ProfileStatsView(GenericAPIView):
    """
    Get profile statistics for a user
    
    GET: Returns follower count, following count, and post count
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserIdSerializer
    
    def get(self, request, user_id):
        # Validate user_id
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        from apps.posts.models import Post
        
        return Response({
            "success": True,
            "data": {
                "followers_count": profile.followers.count(),
                "following_count": profile.following.count(),
                "posts_count": Post.objects.filter(user=user, is_deleted=False).count()
            }
        }, status=status.HTTP_200_OK)


class MyProfileView(GenericAPIView):
    """
    Get detailed profile information for the current user
    
    GET: Returns complete profile data including email and stats
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        
        from apps.posts.models import Post
        
        serializer = ProfileSerializer(profile, context={'request': request})
        
        return Response({
            "success": True,
            "data": {
                **serializer.data,
                "email": request.user.email,
                "phone": request.user.phone,
                "stats": {
                    "followers_count": profile.followers.count(),
                    "following_count": profile.following.count(),
                    "posts_count": Post.objects.filter(user=request.user, is_deleted=False).count()
                }
            }
        }, status=status.HTTP_200_OK)


class UpdateAvatarView(GenericAPIView):
    """
    Update user avatar/profile image
    
    POST: Upload or update profile avatar
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response({
                "success": False,
                "error": "لطفاً یک تصویر انتخاب کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        profile.avatar = avatar
        profile.save()
        
        serializer = ProfileSerializer(profile, context={'request': request})
        
        return Response({
            "success": True,
            "message": "تصویر پروفایل با موفقیت به روز رسانی شد",
            "data": {
                "avatar_url": serializer.data.get('avatar_url')
            }
        }, status=status.HTTP_200_OK)