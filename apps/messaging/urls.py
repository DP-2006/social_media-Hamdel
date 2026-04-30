# apps/messaging/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register('', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:conversation_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='conversation-messages'),
    path('<int:conversation_pk>/messages/mark-read/', MessageViewSet.as_view({'post': 'mark_read'}), name='mark-read'),
]