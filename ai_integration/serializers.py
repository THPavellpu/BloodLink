"""
Serializers for AI integration.
"""
from rest_framework import serializers


class AIQuerySerializer(serializers.Serializer):
    """Serializer for AI chat queries."""
    question = serializers.CharField(max_length=1000)
    context = serializers.CharField(max_length=2000, required=False, allow_blank=True)


class AIResponseSerializer(serializers.Serializer):
    """Serializer for AI chat responses."""
    success = serializers.BooleanField()
    answer = serializers.CharField(required=False, allow_blank=True)
    error = serializers.CharField(required=False, allow_blank=True)
    model = serializers.CharField(required=False, allow_blank=True)
