# apps/blocks/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockViewSet, BlockedUsersMixin

router = DefaultRouter()
router.register('', BlockViewSet, basename='blocks')

urlpatterns = [
    path('', include(router.urls)),
]