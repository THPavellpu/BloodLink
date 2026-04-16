"""
Serializers for notifications.
"""
from rest_framework import serializers
from .models import NotificationToken


class NotificationTokenSerializer(serializers.ModelSerializer):
    """Serializer for FCM notification tokens."""

    class Meta:
        model = NotificationToken
        fields = ['id', 'token', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FCMTokenRegisterSerializer(serializers.Serializer):
    """Serializer for registering FCM tokens."""
    token = serializers.CharField(max_length=500)
