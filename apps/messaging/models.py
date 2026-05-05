# apps/messaging/models.py

from django.db import models
from django.conf import settings
from core.models.base_model import BaseModel



class Conversation(BaseModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    last_message_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Conversation {self.id}"


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender}"



class GroupConversation(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان گروه")
    avatar = models.ImageField(upload_to='groups/', blank=True, null=True, verbose_name="عکس گروه")
    description = models.TextField(max_length=500, blank=True, verbose_name="توضیحات")
    
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='group_conversations',
        verbose_name="اعضا"
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='admin_groups',
        verbose_name="مدیر گروه"
    )
    
    last_message_at = models.DateTimeField(auto_now=True, verbose_name="آخرین پیام")
    last_message_preview = models.CharField(max_length=100, blank=True, verbose_name="پیش‌نمایش آخرین پیام")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ['-last_message_at']
        verbose_name = "گفتگوی گروهی"
        verbose_name_plural = "گفتگوهای گروهی"

    def __str__(self):
        return self.title

    def get_member_count(self):
        return self.members.count()

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    def is_admin(self, user):
        return self.admin == user


class GroupMessage(BaseModel):
    conversation = models.ForeignKey(
        GroupConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="گفتگو"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_group_messages',
        verbose_name="فرستنده"
    )
    content = models.TextField(verbose_name="متن پیام")
    
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده توسط همه؟")
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='read_group_messages',
        blank=True,
        verbose_name="خوانده شده توسط"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "پیام گروهی"
        verbose_name_plural = "پیام‌های گروهی"

    def __str__(self):
        return f"Message from {self.sender} in {self.conversation.title}"

    def mark_as_read(self, user):
        """علامت‌گذاری پیام به عنوان خوانده شده توسط کاربر"""
        if not self.read_by.filter(id=user.id).exists():
            self.read_by.add(user)
            if self.read_by.count() == self.conversation.members.count():
                self.is_read = True
                self.save(update_fields=['is_read'])
            return True
        return False

    def is_read_by_user(self, user):
        """بررسی اینکه آیا پیام توسط کاربر خاصی خوانده شده"""
        return self.read_by.filter(id=user.id).exists()


class GroupMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'مدیر'),
        ('moderator', 'مدیریت'),
        ('member', 'عضو'),
    ]
    
    group = models.ForeignKey(GroupConversation, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_muted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = [['group', 'user']]
    
    def __str__(self):
        return f"{self.user.username} - {self.group.title} ({self.role})"