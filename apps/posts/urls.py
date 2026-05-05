# # apps/posts/urls.py

# from django.urls import path
# from . import views
# urlpatterns = [
#     path('', views.PostListCreateView.as_view(), name='post-list'),
#     path('<str:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
#     path('<str:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list'), 
#     path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
#     path('<str:post_id>/like/', views.LikePostView.as_view(), name='like-post'),  
#     path('<int:post_id>/save/', SavePostView.as_view(), name='save-post'),
#     path('saved/', SavedPostsListView.as_view(), name='saved-posts'),
#     path('<int:post_id>/saved-status/', CheckSavedStatusView.as_view(), name='saved-status'),

# ]






# apps/posts/urls.py (نسخه نهایی)

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    path('<int:post_id>/like/', views.LikeToggleView.as_view(), name='like-toggle'),
    
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    
    path('<int:post_id>/save/', views.SavePostView.as_view(), name='save-post'),
    path('saved/', views.SavedPostsListView.as_view(), name='saved-posts'),
    path('<int:post_id>/saved-status/', views.CheckSavedStatusView.as_view(), name='saved-status'),
]