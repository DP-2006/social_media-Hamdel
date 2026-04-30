# from argparse import Action

# from django.shortcuts import get_object_or_404, render

# # Create your views here.
# # apps/posts/views.py

# from rest_framework import viewsets, status, permissions
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Post, Like, Comment
# from .serializers import PostSerializer

# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.db.models import Count
# from .models import Post, Like
# from .serializers import CommentSerializer, PostSerializer, LikeSerializer
# from core.pagination import StandardPagination
# from django.db import models
# from .models import Comment

# class PostViewSet(viewsets.ModelViewSet):
#     """ViewSet برای پست‌ها با Pagination"""
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardPagination 

#     def get_queryset(self):
#         # نمایش پست‌های کاربرانی که دنبال می‌کنیم + پست‌های خودمان
#         following_ids = self.request.user.following.values_list('following_id', flat=True)
#         return Post.objects.filter(
#             models.Q(user__in=following_ids) | models.Q(user=self.request.user)
#         ).select_related('user').prefetch_related('likes').order_by('-created_at')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class LikeViewSet(viewsets.ModelViewSet):
#     """ViewSet برای لایک‌ها با Pagination"""
#     serializer_class = LikeSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = StandardPagination  

#     def get_queryset(self):
#         return Like.objects.filter(post_id=self.kwargs['post_pk']).select_related('user')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)








# class CommentViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet برای مدیریت کامنت‌ها
    
#     Endpoints:
#     - GET    /api/posts/{post_id}/comments/        → لیست کامنت‌ها
#     - POST   /api/posts/{post_id}/comments/       → ایجاد کامنت
#     - GET    /api/posts/{post_id}/comments/{id}/  → جزئیات کامنت
#     - PUT    /api/posts/{post_id}/comments/{id}/  → ویرایش کامنت
#     - DELETE /api/posts/{post_id}/comments/{id}/  → حذف کامنت
#     """
    
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """دریافت کامنت‌های پست"""
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
        
#         # فقط کامنت‌های اصلی (بدون ریپلای)
#         return Comment.objects.filter(
#             post=post,
#             parent=None  # فقط کامنت‌های اصلی
#         ).select_related('user').prefetch_related('replies__user')
    
#     def get_serializer_context(self):
#         """ارسال context به serializer"""
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context
    
#     def create(self, request, *args, **kwargs):
#         """ایجاد کامنت جدید"""
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
        
#         # افزودن post به داده‌ها
#         data = request.data.copy()
#         data['post'] = str(post.id)
        
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response({
#             "success": True,
#             "message": "کامنت با موفقیت ثبت شد",
#             "data": serializer.data
#         }, status=status.HTTP_201_CREATED)
    
#     def update(self, request, *args, **kwargs):
#         """ویرایش کامنت"""
#         instance = self.get_object()
        
#         # بررسی مالکیت کامنت
#         if instance.user != request.user:
#             return Response({
#                 "success": False,
#                 "error": "شما مجاز به ویرایش این کامنت نیستید"
#             }, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response({
#             "success": True,
#             "message": "کامنت با موفقیت ویرایش شد",
#             "data": serializer.data
#         })
    
#     def destroy(self, request, *args, **kwargs):
#         """حذف کامنت"""
#         instance = self.get_object()
        
#         # بررسی مالکیت کامنت یا ادمین بودن
#         if instance.user != request.user and not request.user.is_staff:
#             return Response({
#                 "success": False,
#                 "error": "شما مجاز به حذف این کامنت نیستید"
#             }, status=status.HTTP_403_FORBIDDEN)
        
#         instance.delete()
        
#         return Response({
#             "success": True,
#             "message": "کامنت با موفقیت حذف شد"
#         }, status=status.HTTP_204_NO_CONTENT)
    
#     @Action(detail=True, methods=['get'])
#     def replies(self, request, post_id=None, pk=None):
#         """دریافت ریپلای‌های یک کامنت"""
#         comment = self.get_object()
#         replies = comment.replies.select_related('user').all()
        
#         serializer = ReplySerializer(replies, many=True)
        
#         return Response({
#             "success": True,
#             "data": serializer.data
#         })
    
#     @Action(detail=False, methods=['post'])
#     def reply(self, request, post_id=None):
#         """ایجاد ریپلای برای یک کامنت"""
#         post = get_object_or_404(Post, id=post_id)
#         parent_id = request.data.get('parent')
        
#         if not parent_id:
#             return Response({
#                 "success": False,
#                 "error": "شناسه کامنت والد الزامی است"
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             parent_comment = Comment.objects.get(id=parent_id, post=post)
#         except Comment.DoesNotExist:
#             return Response({
#                 "success": False,
#                 "error": "کامنت والد یافت نشد"
#             }, status=status.HTTP_404_NOT_FOUND)
        
#         # بررسی سطح ریپلای
#         if parent_comment.parent is not None:
#             return Response({
#                 "success": False,
#                 "error": "فقط یک سطح ریپلای مجاز است"
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         data = request.data.copy()
#         data['post'] = str(post.id)
#         data['parent'] = str(parent_comment.id)
        
#         serializer = CommentSerializer(data=data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response({
#             "success": True,
#             "message": "ریپلای با موفقیت ثبت شد",
#             "data": serializer.data
#         }, status=status.HTTP_201_CREATED)



# ############################################################################################################
# # apps/posts/views.py

# class PostViewSet(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def get_queryset(self):
#         return Post.objects.all().prefetch_related('media_files', 'likes', 'comments')
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
#     @action(detail=True, methods=['post'])
#     def like(self, request, pk=None):
#         post = self.get_object()
#         like, created = Like.objects.get_or_create(user=request.user, post=post)
        
#         if not created:
#             like.delete()
#             return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        
#         return Response({'status': 'liked', 'likes_count': post.likes.count()})
    
#     @action(detail=True, methods=['post'])
#     def unlike(self, request, pk=None):
#         post = self.get_object()
#         deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        
#         if deleted:
#             return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        
#         return Response({'status': 'not_liked'}, status=status.HTTP_400_BAD_REQUEST

# #################################################################################################################################

# class PostListCreateView(generics.ListCreateAPIView):
#     """لیست پست‌ها و ساخت پست جدید"""
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return Post.objects.all().order_by('-created_at')
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """مشاهده، ویرایش و حذف پست"""
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return Post.objects.all()
    
#     def perform_update(self, serializer):
#         serializer.save()
    
#     def perform_destroy(self, instance):
#         instance.delete()


# class CommentListCreateView(generics.ListCreateAPIView):
#     """لیست کامنت‌های یک پست و ساخت کامنت جدید"""
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         post_id = self.kwargs.get('post_id')
#         return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
#     def perform_create(self, serializer):
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
#         serializer.save(author=self.request.user, post=post)


# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """مشاهده، ویرایش و حذف کامنت"""
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return Comment.objects.all()
    
#     def perform_destroy(self, instance):
#         instance.delete()


# class LikePostView(APIView):
#     """لایک و آنلایک کردن پست"""
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request, post_id):
#         post = get_object_or_404(Post, id=post_id)
#         like, created = Like.objects.get_or_create(
#             post=post,
#             user=request.user
#         )
        
#         if created:
#             return Response({
#                 'status': 'liked',
#                 'message': 'پست با موفقیت لایک شد'
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({
#             'status': 'already_liked',
#             'message': 'شما قبلاً این پست را لایک کرده‌اید'
#         }, status=status.HTTP_200_OK)
    
#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, id=post_id)
#         deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        
#         if deleted:
#             return Response({
#                 'status': 'unliked',
#                 'message': 'لایک پست حذف شد'
#             }, status=status.HTTP_200_OK)
        
#         return Response({
#             'status': 'not_liked',
#             'message': 'شما این پست را لایک نکرده‌اید'
#         }, status=status.HTTP_400_BAD_REQUEST)





















# apps/posts/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all()


class CommentListCreateView(generics.ListCreateAPIView):
    """لیست کامنت‌های یک پست و ساخت کامنت جدید"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """مشاهده، ویرایش و حذف کامنت"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.all()


class LikePostView(APIView):
    """لایک و آنلایک کردن پست"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )
        
        if created:
            return Response({
                'status': 'liked',
                'message': 'پست با موفقیت لایک شد'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'already_liked',
            'message': 'شما قبلاً این پست را لایک کرده‌اید'
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        
        if deleted:
            return Response({
                'status': 'unliked',
                'message': 'لایک پست حذف شد'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'not_liked',
            'message': 'شما این پست را لایک نکرده‌اید'
        }, status=status.HTTP_400_BAD_REQUEST)
