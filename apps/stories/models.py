from django.db import models

# Create your models here.
# apps/stories/models.py

from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel


class Story(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )
    image = models.ImageField(upload_to='stories/')
    caption = models.CharField(max_length=150, blank=True)
    expires_at = models.DateTimeField()  
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"Story by {self.user} - {self.created_at}"

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at


class StoryView(BaseModel):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='views'
    )
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='viewed_stories'
    )

    class Meta:
        unique_together = [['story', 'viewer']] 

    def __str__(self):
        return f"{self.viewer} viewed story {self.story.id}"
    
