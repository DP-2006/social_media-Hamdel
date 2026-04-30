from django.contrib import admin

# Register your models here.
# apps/follows/admin.py

from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['follower', 'following']
    search_fields = ['follower__phone', 'following__phone']