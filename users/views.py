"""
Views for user authentication and profile management.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer,
    UserUpdateSerializer, LocationUpdateSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view."""
    serializer_class = CustomTokenObtainPairSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for authentication operations.
    Handles user registration and authentication.
    """

    def get_permissions(self):
        """
        Assign permissions based on action.
        - register: Public (AllowAny)
        - Other actions: Require authentication
        """
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user.
        
        POST /api/register/
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for user profile management.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        Get current user profile.
        
        GET /api/profile/
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update user profile.
        
        PUT /api/profile/update/
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Profile updated successfully',
                    'user': UserSerializer(request.user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def location(self, request):
        """
        Update user location.
        
        POST /api/user/location/
        """
        serializer = LocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            request.user.latitude = serializer.validated_data['latitude']
            request.user.longitude = serializer.validated_data['longitude']
            request.user.location_name = serializer.validated_data['location_name']
            request.user.save()
            return Response(
                {
                    'message': 'Location updated successfully',
                    'user': UserSerializer(request.user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
