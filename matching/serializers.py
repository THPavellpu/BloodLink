"""
Serializers for donor matching.
"""
from rest_framework import serializers
from users.serializers import UserSerializer


class DonorMatchSerializer(serializers.Serializer):
    """Serializer for matched donors with their scores."""
    donor = UserSerializer()
    score = serializers.IntegerField()
    distance = serializers.FloatField()


class BloodMatchQuerySerializer(serializers.Serializer):
    """Serializer for blood match query parameters."""
    blood_group = serializers.CharField(max_length=5)
    latitude = serializers.FloatField(min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(min_value=-180.0, max_value=180.0)
    limit = serializers.IntegerField(default=50, min_value=1, max_value=200)
