from django.contrib import admin

# Register your models here.
# apps/profiles/admin.py

# apps/profiles/admin.py

# from django.contrib import admin
# from .models import Profile

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'display_name', 'bio', 'created_at', 'is_active']
#     list_filter = ['is_active', 'created_at']
#     search_fields = ['display_name', 'user__phone', 'user__username']
#     raw_id_fields = ['user']
#     readonly_fields = ['id', 'created_at', 'updated_at']





from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'is_private', 'is_active', 'created_at']
    list_filter = ['is_private', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__phone', 'display_name']
    raw_id_fields = ['user']
    readonly_fields = ['id', 'created_at', 'updated_at']