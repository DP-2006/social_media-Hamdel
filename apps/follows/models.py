# apps/follows/models.py

from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel


class Follow(BaseModel):
    """مدل فالو - کاربر A کاربر B را فالو می‌کند"""
    
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'  # افرادی که این کاربر فالو می‌کند
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'  # افرادی که این کاربر را فالو کرده‌اند
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['follower', 'following']]
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')),
                name='cannot_follow_self'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"