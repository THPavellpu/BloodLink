"""
Serializers for blood requests.
"""
from rest_framework import serializers
from .models import BloodRequest
from users.serializers import UserSerializer


class BloodRequestSerializer(serializers.ModelSerializer):
    """Serializer for BloodRequest model."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodRequest
        fields = [
            'id', 'user', 'blood_group', 'latitude', 'longitude',
            'location_name', 'urgency', 'message', 'is_fulfilled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class BloodRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating blood requests."""

    class Meta:
        model = BloodRequest
        fields = [
            'blood_group', 'latitude', 'longitude',
            'location_name', 'urgency', 'message'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BloodRequestUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating blood requests."""

    class Meta:
        model = BloodRequest
        fields = [
            'blood_group', 'latitude', 'longitude',
            'location_name', 'urgency', 'message', 'is_fulfilled'
        ]
