


# apps/ml/urls.py
from django.urls import path
from . import views




# # apps/ml/urls.py - کپی کن جایگزین کن
# from django.urls import path
# from . import views

# urlpatterns = [
#     # سلامت سرویس
#     path('health/', views.HealthCheckView.as_view(), name='health'),
    
#     # تست ساده
#     path('test/', views.TestAIView.as_view(), name='test'),
    
#     # لیست کاربران
#     path('users/', views.UserListView.as_view(), name='user-list'),
#     # تحلیل کاربر
#     path('users/<int:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
#     path('users/', views.UserListView.as_view(), name='user-list'),
#     # این خط مهمه - برای پشتیبانی از UUID
#     # تحلیل کاربر با آیدی
#     path('users/<str:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
#     # تحلیل کاربر با شماره تلفن
#     path('users/analyze-by-phone/', views.AnalyzeAnyUserView.as_view(), name='analyze-by-phone'),
# ]















     





from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:user_id>/analyze/', views.AdminAnalyzeUserView.as_view(), name='analyze-user'),
    path('users/<str:user_id>/analyze/', views.AdminAnalyzeUserView.as_view(), name='analyze-user'),
    path('explore/smart/', views.ExploreFeedView.as_view(), name='explore-smart'),     
    path('explore/refresh/', views.RefreshExploreView.as_view(), name='explore-refresh')
    #path('test/', views.TestAIView.as_view(), name='test'),
]