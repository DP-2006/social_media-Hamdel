from django.db import models

# Create your models here.
# apps/blocks/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from core.models.base_model import BaseModel


class Block(BaseModel):
    
    blocker = models.ForeignKey(#بلاک کننده  )(فاعل )
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_users_set',
        verbose_name='bloke'
    )
    blocked = models.ForeignKey( #بلاک شونده )(مفعول)
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by_set',
        verbose_name='bloke object'
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='دلیل'
    )
    
    class Meta:
        unique_together = [['blocker', 'blocked']]
        verbose_name = 'Blok'
        verbose_name_plural = 'Bloks'
        indexes = [
            models.Index(fields=['blocker', '-created_at']),
            models.Index(fields=['blocked', '-created_at']),
        ]
    
    def clean(self):
        if self.blocker == self.blocked:
            raise ValidationError("خود درگیری داری ؟؟")
    
    def __str__(self):
        return f"{self.blocker} → {self.blocked}"