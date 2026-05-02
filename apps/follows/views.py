# apps/follows/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Follow
from .serializers import FollowSerializer, FollowerListSerializer, FollowingListSerializer

User = get_user_model()


class FollowToggleView(APIView):
    """
    فالو/آنفالو کردن کاربر
    POST /api/follows/toggle/<user_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        
        # جلوگیری از فالو کردن خود
        if request.user == target_user:
            return Response({
                "success": False,
                "error": "نمی‌توانید خودتان را فالو کنید"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # بررسی وجود رابطه فالو
            follow = Follow.objects.filter(
                follower=request.user,
                following=target_user
            ).first()
            
            if follow:
                # آنفالو کردن
                follow.delete()
                return Response({
                    "success": True,
                    "action": "unfollowed",
                    "message": f"شما {target_user.username} را آنفالو کردید"
                }, status=status.HTTP_200_OK)
            else:
                # فالو کردن
                follow = Follow.objects.create(
                    follower=request.user,
                    following=target_user
                )
                serializer = FollowSerializer(follow)
                return Response({
                    "success": True,
                    "action": "followed",
                    "message": f"شما اکنون {target_user.username} را فالو می‌کنید",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)


class FollowersListView(generics.ListAPIView):
    """
    لیست فالوورهای یک کاربر
    GET /api/follows/users/<user_id>/followers/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # دریافت فالوورها با select_related برای بهینه‌سازی
        follows = Follow.objects.filter(
            following=user
        ).select_related('follower', 'follower__profile').order_by('-created_at')
        
        results = []
        for follow in follows:
            follower = follow.follower
            profile = getattr(follower, 'profile', None)
            results.append({
                "id": str(follower.id),
                "username": follower.username,
                "display_name": profile.display_name if profile else follower.username,
                "profile_image": profile.profile_image.url if profile and profile.profile_image else None,
                "followed_at": follow.created_at
            })
        
        return Response({
            "success": True,
            "count": len(results),
            "data": results
        }, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    لیست افرادی که کاربر فالو می‌کند
    GET /api/follows/users/<user_id>/following/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # دریافت فالوینگ‌ها با select_related برای بهینه‌سازی
        follows = Follow.objects.filter(
            follower=user
        ).select_related('following', 'following__profile').order_by('-created_at')
        
        results = []
        for follow in follows:
            following = follow.following
            profile = getattr(following, 'profile', None)
            results.append({
                "id": str(following.id),
                "username": following.username,
                "display_name": profile.display_name if profile else following.username,
                "profile_image": profile.profile_image.url if profile and profile.profile_image else None,
                "followed_at": follow.created_at
            })
        
        return Response({
            "success": True,
            "count": len(results),
            "data": results
        }, status=status.HTTP_200_OK)


class FollowCountView(APIView):
    """
    دریافت تعداد فالوور و فالوینگ
    GET /api/follows/users/<user_id>/counts/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        followers_count = Follow.objects.filter(following=user).count()
        following_count = Follow.objects.filter(follower=user).count()
        
        return Response({
            "success": True,
            "data": {
                "followers_count": followers_count,
                "following_count": following_count
            }
        }, status=status.HTTP_200_OK)


class CheckFollowStatusView(APIView):
    """
    بررسی وضعیت فالو
    GET /api/follows/check/?target_id=<user_id>
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        target_id = request.query_params.get('target_id')
        
        if not target_id:
            return Response({
                "success": False,
                "error": "target_id الزامی است"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        target_user = get_object_or_404(User, id=target_id)
        
        is_following = Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).exists()
        
        is_followed_by = Follow.objects.filter(
            follower=target_user,
            following=request.user
        ).exists()
        
        return Response({
            "success": True,
            "data": {
                "is_following": is_following,
                "is_followed_by": is_followed_by,
                "is_mutual": is_following and is_followed_by
            }
        }, status=status.HTTP_200_OK)