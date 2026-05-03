# apps/follows/models.py

from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel


class Follow(BaseModel):
    
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_set',  # افرادی که این کاربر فالو می‌کند
        verbose_name='follower'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower_set',  # افرادی که این کاربر را فالو کرده‌اند
        verbose_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    class Meta:
        db_table = 'follows_follow'
        verbose_name = 'follow'
        verbose_name_plural = 'follower'
        
        indexes = [
            models.Index(fields=['follower', '-created_at'], 
                        name='idx_follower_created'),
            models.Index(fields=['following', '-created_at'], 
                        name='idx_following_created'),
        ]
        
       
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'], 
                name='unique_follow_relationship'
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')),
                name='cannot_follow_self'
            ),
        ]
        
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    @classmethod
    def get_followers_with_users(cls, user_id):
        return cls.objects.select_related('follower').filter(following_id=user_id)
    
    @classmethod
    def get_following_with_users(cls, user_id):
        return cls.objects.select_related('following').filter(follower_id=user_id)
    
    @classmethod
    def check_follow_status(cls, follower_id, following_id):
        return cls.objects.filter(
            follower_id=follower_id, 
            following_id=following_id
        ).exists()