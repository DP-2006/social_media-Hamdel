# apps/messaging/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'conversations/(?P<conversation_pk>[0-9]+)/messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns = [
    # مسیرهای ViewSet (قبلی)
    path('', include(router.urls)),
    
    # مسیرهای جدید دستیار هوشمند
    path('analyze-target/<int:user_id>/', views.TargetAnalysisView.as_view(), name='analyze-target'),
    path('suggestions/opening/<int:user_id>/', views.OpeningMessageSuggestionsView.as_view(), name='opening-suggestions'),
    path('suggestions/reply/', views.ReplySuggestionView.as_view(), name='reply-suggestion'),
    path('icebreakers/<int:user_id>/', views.IceBreakerTopicsView.as_view(), name='icebreakers'),
    path('start-with-ai/', views.StartConversationWithAIAssistView.as_view(), name='start-with-ai'),
]