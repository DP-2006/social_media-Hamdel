
# from django.db import models
# from django.conf import settings
# import uuid

# class Profile(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='profile'
#     )
#     display_name = models.CharField(max_length=100, blank=True, default='')
#     bio = models.TextField(max_length=500, blank=True, default='')
#     #avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         default='defaults/default_avatar.png',
#         blank=True
#     )
#     is_private = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return f"پروفایل {self.user.username}"
    
#     @property
#     def followers_count(self):
#         return self.followers.count()
    
#     @property
#     def following_count(self):
#         return self.following.count()
from django.db import models
from django.conf import settings
import uuid
# وارد کردن مدل Follow برای کوئری زدن مستقیم
from apps.follows.models import Follow

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True, default='')
    profile_image = models.ImageField(
        upload_to='profiles/',
        default='defaults/default_avatar.png',
        blank=True
    )
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"پروفایل {self.user.username}"

    @property
    def followers(self):
        """
        لیست کاربران (User objects) که این پروفایل را فالو کرده‌اند.
        """
        # کسانی که following_id برابر با user_id این پروفایل است
        # select_related('follower') باعث می‌شود اطلاعات کاربر فالوکننده در یک کوئری لود شود
        return Follow.objects.filter(following=self.user).select_related('follower').values_list('follower', flat=True)

    @property
    def following(self):
        """
        لیست کاربران (User objects) که این پروفایل آن‌ها را فالو کرده است.
        """
        # کسانی که follower_id برابر با user_id این پروفایل است
        return Follow.objects.filter(follower=self.user).select_related('following').values_list('following', flat=True)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()