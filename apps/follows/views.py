# apps/follows/views.py

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer, FollowerListSerializer

User = get_user_model()


class FollowerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerListSerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Follow.objects.select_related('follower').filter(
            following_id=user_id
        ).only('id', 'created_at', 'follower__id', 'follower__username', 'follower__email')


class FollowingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerListSerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Follow.objects.select_related('following').filter(
            follower_id=user_id
        ).only('id', 'created_at', 'following__id', 'following__username', 'following__email')


class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        follower = request.user
        following = get_object_or_404(User, id=user_id)
        
        if follower.id == following.id:
            return Response(
                {'error': 'you cant follow her !'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )
        
        if created:
            return Response(
                {'message': f'you {following.username} follow'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'you follow this user in past'}, 
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        deleted_count, _ = Follow.objects.filter(
            follower=request.user,
            following_id=user_id
        ).delete()
        
        if deleted_count > 0:
            return Response(
                {'message': 'sucsse unfloow'}, 
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'you dot follow this user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )