from django.contrib import admin

# Register your models here.
# apps/stories/admin.py

from django.contrib import admin
from .models import Story, StoryView

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'caption', 'expires_at', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    raw_id_fields = ['user']

@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'viewer', 'created_at']
    raw_id_fields = ['story', 'viewer']