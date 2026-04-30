from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserProfileSerializer

User = get_user_model()

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        serializer = ProfileUpdateSerializer(
            profile, 
            data=request.data,
            partial=False
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "پروفایل با موفقیت بروزرسانی شد",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        """بروزرسانی جزئی پروفایل"""
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        serializer = ProfileUpdateSerializer(
            profile, 
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "پروفایل با موفقیت بروزرسانی شد",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PublicProfileView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        """دریافت پروفایل عمومی یک کاربر"""
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        # اگر پروفایل خصوصی است و کاربر دنبال نمی‌کند
        if profile.is_private and not request.user == user:
            # بررسی کند که آیا کاربر دنبال می‌کند یا خیر
            is_following = profile.followers.filter(id=request.user.id).exists()
            if not is_following:
                return Response({
                    "success": False,
                    "error": "این حساب کاربری خصوصی است"
                }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProfileSerializer(profile)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        target_profile = get_object_or_404(Profile, user=target_user)
        
        # نمی‌توان خودت را دنبال کنی
        if request.user == target_user:
            return Response({
                "success": False,
                "error": "نمی‌توانید خودتان را دنبال کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # دنبال کردن یا لغو دنبال کردن
        if target_profile.followers.filter(id=request.user.id).exists():
            # لغو دنبال کردن
            target_profile.followers.remove(request.user)
            return Response({
                "success": True,
                "action": "unfollowed",
                "message": f"دنبال کردن {target_user.username} لغو شد"
            }, status=status.HTTP_200_OK)
        else:
            # دنبال کردن
            target_profile.followers.add(request.user)
            return Response({
                "success": True,
                "action": "followed",
                "message": f"اکنون {target_user.username} را دنبال می‌کنید"
            }, status=status.HTTP_200_OK)


class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        followers = profile.followers.all()
        followers_data = []
        
        for follower in followers:
            follower_profile = Profile.objects.get(user=follower)
            followers_data.append({
                "id": follower.id,
                "username": follower.username,
                "display_name": follower_profile.display_name,
                "avatar": follower_profile.avatar.url if follower_profile.avatar else None
            })
        
        return Response({
            "success": True,
            "count": len(followers_data),
            "data": followers_data
        }, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        following = profile.following.all()
        following_data = []
        
        for followed in following:
            followed_profile = Profile.objects.get(user=followed)
            following_data.append({
                "id": followed.id,
                "username": followed.username,
                "display_name": followed_profile.display_name,
                "avatar": followed_profile.avatar.url if followed_profile.avatar else None
            })
        
        return Response({
            "success": True,
            "count": len(following_data),
            "data": following_data
        }, status=status.HTTP_200_OK)


class SearchUserView(APIView):
    """
    جستجوی کاربران
    GET /api/profiles/search/?q=username
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({
                "success": False,
                "error": "لطفاً عبارت جستجو را وارد کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.filter(username__icontains=query)[:20]
        
        results = []
        for user in users:
            profile = Profile.objects.get(user=user)
            results.append({
                "id": user.id,
                "username": user.username,
                "display_name": profile.display_name,
                "avatar": profile.avatar.url if profile.avatar else None,
                "is_private": profile.is_private
            })
        
        return Response({
            "success": True,
            "count": len(results),
            "data": results
        }, status=status.HTTP_200_OK)