from django.contrib import admin

# Register your models here.
# apps/hashtags/admin.py

from django.contrib import admin
from .models import Hashtag, PostHashtag

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'usage_count', 'created_at']
    list_filter = ['usage_count']
    search_fields = ['name']
    ordering = ['-usage_count']

@admin.register(PostHashtag)
class PostHashtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'hashtag', 'created_at']
    raw_id_fields = ['post', 'hashtag']