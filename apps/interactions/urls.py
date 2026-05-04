# apps/interactions/urls.py

from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('explore/', views.ExploreFeedView.as_view(), name='explore-feed'),
]