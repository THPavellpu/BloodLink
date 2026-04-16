"""
Serializers for User model and authentication.
"""
import logging
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable

logger = logging.getLogger(__name__)
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'phone', 'blood_group',
            'latitude', 'longitude', 'location_name', 'is_available',
            'last_donation_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with comprehensive validation.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'password', 'password2',
            'phone', 'blood_group', 'location_name'
        ]

    def validate_username(self, value):
        """Validate that username doesn't already exist."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        """Validate that email doesn't already exist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_phone(self, value):
        """Validate that phone doesn't already exist if provided."""
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate(self, data):
        """Validate password matching."""
        if data.get('password') != data.pop('password2', None):
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return data

    def _geocode_location(self, location_name):
        """
        Convert location name to latitude and longitude using Nominatim.
        
        Returns: (latitude, longitude) or (None, None) if geocoding fails
        """
        if not location_name:
            return None, None

        try:
            geolocator = Nominatim(user_agent="bloodlink_app")
            location = geolocator.geocode(location_name, timeout=10)
            
            if location:
                logger.info(f"Successfully geocoded location: {location_name}")
                return location.latitude, location.longitude
            else:
                logger.warning(f"Location not found in geocoder: {location_name}")
                return None, None
                
        except (GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable) as e:
            logger.warning(f"Geocoding service error for '{location_name}': {str(e)}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error during geocoding of '{location_name}': {str(e)}")
            return None, None

    def create(self, validated_data):
        """
        Create user with comprehensive error handling.
        
        Safely handles:
        - Geolocation failures (stores None for coords)
        - Database constraint violations
        - Missing optional fields
        """
        location_name = validated_data.get('location_name')
        
        # Convert location to coordinates (fails gracefully)
        latitude, longitude = self._geocode_location(location_name)

        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                phone=validated_data.get('phone'),
                blood_group=validated_data.get('blood_group'),
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
            )
            logger.info(f"User created successfully: {user.username}")
            return user
            
        except IntegrityError as e:
            logger.error(f"Integrity constraint violated during user creation: {str(e)}")
            raise serializers.ValidationError(
                "A user with this username, email, or phone already exists."
            )
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            raise serializers.ValidationError(
                "An error occurred during registration. Please try again."
            )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

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
        data['user'] = UserSerializer(self.user).data
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'phone', 'blood_group',
            'latitude', 'longitude', 'location_name', 'is_available'
        ]


class LocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    location_name = serializers.CharField(max_length=255)