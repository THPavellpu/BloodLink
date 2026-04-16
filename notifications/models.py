"""
Models for notifications.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationToken(models.Model):
    """Model to store FCM tokens for push notifications."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fcm_token')
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FCM Token'
        verbose_name_plural = 'FCM Tokens'

    def __str__(self):
        return f"{self.user.username} - FCM Token"
