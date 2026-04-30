# # apps/ml/urls.py

# from django.urls import path
# from . import views
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PersonalityAnalysisViewSet

# router = DefaultRouter()
# router.register('personality', PersonalityAnalysisViewSet, basename='personality')


# # urlpatterns = [
# #     # فید شخصی‌سازی شده
# #     #path('feed/personalized/', views.PersonalizedFeedView.as_view(), name='personalized_feed'),
    
# #     # تعدیل محتوا
# #     path('moderate/', views.ContentModerationView.as_view(), name='moderate_content'),
    
# #     # آموزش مدل
# #     path('train/', views.TrainModelView.as_view(), name='train_model'),
    
# #     # وضعیت سلامت
# #     path('health/', views.ModelHealthView.as_view(), name='ml_health'),
    
# #     # ⭐ شخصیت‌شناسی کاربر (جدید)
# #     path('personality/analyze/', views.UserPersonalityAnalysisView.as_view(), name='personality_analyze'),
# #     path('personality/analyze/<int:user_id>/', views.UserPersonalityAnalysisView.as_view(), name='personality_analyze_user'),
# #     path('personality/analyze/', UserPersonalityAPIView.as_view(), name='personality_analyze'),
# #     path('personality/analyze/<int:user_id>/', UserPersonalityAPIView.as_view(), name='personality_analyze_user'),
# #     path('users/', views.AnalyzeUserView.as_view(), name='user-list'),
# #     path('users/<int:user_id>/analyze/', views.AnalyzeUserView.as_view(), name='analyze-user'),
# #     path('users/', views.AnalyzeUserView.as_view(), name='user-list'),
# #     path('users/<int:user_id>/analyze/', views.AnalyzeUserView.as_view(), name='analyze-user'),
# #     path('test/', views.TestAIView.as_view(), name='test'),
# #     path('health/', views.TestAIView.as_view(), name='health'),


# # apps/ml/urls.py - کپی کن جایگزین کن
# from django.urls import path
# from . import views

# urlpatterns = [
#     # مسیرهای تحلیل کاربر
#     path('users/', views.AnalyzeUserView.as_view(), name='user-list'),
#     path('users/<int:user_id>/analyze/', views.AnalyzeUserView.as_view(), name='analyze-user'),
    
#     # مسیرهای تست و سلامت
#     path('test/', views.TestAIView.as_view(), name='test'),
#     path('health/', views.TestAIView.as_view(), name='health'),



#     path('personality/analyze-with-ai/', 
#          PersonalityAnalysisWithAIView.as_view(), 
#          name='personality_analyze_with_ai'),
    






# # apps/ml/urls.py - کپی کن جایگزین کن
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('users/', views.AnalyzeUserView.as_view(), name='user-list'),
#     path('users/<int:user_id>/analyze/', views.AnalyzeUserView.as_view(), name='analyze-user'),
#     path('test/', views.TestAIView.as_view(), name='test'),
#     path('health/', views.TestAIView.as_view(), name='health'),


#          path('ollama/test/', 
#           OllamaTestView.as_view(), 
#           name='ollama_test'),
    
#      path('ollama/generate/', 
#          OllamaTestView.as_view(), 
#            name='ollama_generate'),

# ]

# # ]




# apps/ml/urls.py
from django.urls import path
from . import views

# urlpatterns = [
#     # سلامت سرویس
#     path('health/', views.HealthCheckView.as_view(), name='health'),
    
#     # تست سریع اتصال
#     path('test/', views.QuickTestView.as_view(), name='quick-test'),
    
#     # لیست کاربران
#     path('users/', views.UserListView.as_view(), name='user-list'),
    
#     # تحلیل کاربر با AI
#     path('users/<int:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
# ]





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








# apps/ml/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('health/', views.HealthCheckView.as_view(), name='health'),
#     path('test/', views.TestAIView.as_view(), name='test'),
#     path('users/', views.UserListView.as_view(), name='user-list'),
#     path('users/<str:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
#     path('users/<str:user_id>/files/', views.AnalyzeUserFilesView.as_view(), name='analyze-user-files'),
#     path('users/analyze-by-phone/', views.AnalyzeAnyUserView.as_view(), name='analyze-by-phone'),
#     path('analyze/<str:user_id>/', views.AdminAnalyzeUserView.as_view(), name='admin-analyze-user'),

    

# ]








# # apps/ml/urls.py
# from django.urls import path
# from . import views

#  urlpatterns = [path('health/', views.HealthCheckView.as_view(), name='health'),
#      path('test/', views.TestAIView.as_view(), name='test'),
#      path('users/', views.UserListView.as_view(), name='user-list'),
#      path('users/<str:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
#      path('users/<str:user_id>/files/', views.AnalyzeUserFilesView.as_view(), name='analyze-user-files'),
#      path('users/analyze-by-phone/', views.AnalyzeAnyUserView.as_view(), name='analyze-by-phone'),
#      path('analyze/<str:user_id>/', views.AdminAnalyzeUserView.as_view(), name='admin-analyze-user'),
# ]
     


# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('health/', views.HealthCheckView.as_view(), name='health'),
#     # path('test/', views.TestAIView.as_view(), name='test'),
#     # path('users/', views.UserListView.as_view(), name='user-list'),
#     # path('users/<str:user_id>/analyze/', views.AnalyzeUserWithAIView.as_view(), name='analyze-user'),
#     # path('users/<str:user_id>/files/', views.AnalyzeUserFilesView.as_view(), name='analyze-user-files'),
#     # path('users/analyze-by-phone/', views.AnalyzeAnyUserView.as_view(), name='analyze-by-phone'),
# ]






from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:user_id>/analyze/', views.AdminAnalyzeUserView.as_view(), name='analyze-user'),
    path('users/<str:user_id>/analyze/', views.AdminAnalyzeUserView.as_view(), name='analyze-user'),
    #path('test/', views.TestAIView.as_view(), name='test'),
]