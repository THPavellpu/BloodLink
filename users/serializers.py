"""
Serializers for User model and authentication.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name', 'phone', 'blood_group',
            'latitude', 'longitude', 'location_name', 'is_available',
            'last_donation_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'name', 'password', 'password2',
            'phone', 'blood_group', 'latitude', 'longitude', 'location_name'
        ]

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return data

    from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def create(self, validated_data):
    location_name = validated_data.get('location_name')

    latitude = None
    longitude = None

    if location_name:
        try:
            geolocator = Nominatim(user_agent="bloodlink_app")

            location = geolocator.geocode(location_name, timeout=10)

            if location:
                latitude = location.latitude
                longitude = location.longitude

        except (GeocoderTimedOut, GeocoderServiceError):
            # Fail silently (very important for production)
            pass

    user = User.objects.create_user(
        username=validated_data.get('username'),
        email=validated_data.get('email'),
        password=validated_data.get('password'),
        first_name=validated_data.get('name', ''),
        phone=validated_data.get('phone'),
        blood_group=validated_data.get('blood_group'),
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
    )

    return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user data."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['blood_group'] = user.blood_group
        token['is_available'] = user.is_available
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = UserSerializer(user).data
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""

    class Meta:
        model = User
        fields = [
            'email', 'name', 'phone', 'blood_group',
            'latitude', 'longitude', 'location_name', 'is_available'
        ]


class LocationUpdateSerializer(serializers.Serializer):
    """Serializer for updating user location."""
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    location_name = serializers.CharField(max_length=255)
