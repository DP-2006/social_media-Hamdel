from django.contrib import admin

# Register your models here.
# apps/blocks/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'blocker_link', 'blocked_link', 'reason', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username', 'reason']
    raw_id_fields = ['blocker', 'blocked']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ("user", {
            "fields": ("blocker", "blocked")
        }),
        ("information ", {
            "fields": ("reason",)
        }),
        ("TIME", {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    def blocker_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.blocker.id])
        return format_html('<a href="{}">{}</a>', url, obj.blocker.username)
    blocker_link.short_description = 'bloker object'
    blocker_link.admin_order_field = 'blocker__username'
    
    def blocked_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.blocked.id])
        return format_html('<a href="{}">{}</a>', url, obj.blocked.username)
    blocked_link.short_description = 'blokerd'
    blocked_link.admin_order_field = 'blocked__username'