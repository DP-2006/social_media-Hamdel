# apps/posts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # پست‌ها
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # کامنت‌ها
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # لایک‌ها
    path('<int:post_id>/like/', views.LikePostView.as_view(), name='like-post'),
]