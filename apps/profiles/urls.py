from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ProfileView.as_view(), name='profile-me'),
    
    path('<uuid:user_id>/', views.PublicProfileView.as_view(), name='profile-public'),
    
    path('<uuid:user_id>/follow/', views.FollowToggleView.as_view(), name='profile-follow'),
    
    path('<uuid:user_id>/followers/', views.FollowersListView.as_view(), name='profile-followers'),
    
    path('<uuid:user_id>/following/', views.FollowingListView.as_view(), name='profile-following'),
    
    path('search/', views.SearchUserView.as_view(), name='profile-search'),
]