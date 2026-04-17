"""
Views for user authentication and profile management.
"""
import logging
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

logger = logging.getLogger(__name__)
User = get_user_model()


# ------------------ LOGIN ------------------

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ------------------ AUTH ------------------

class AuthViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"New user registered: {user.username}")

                return Response(
                    {
                        'message': 'User registered successfully',
                        'user': UserSerializer(user).data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Something went wrong'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ------------------ USER PROFILE ------------------

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # ✅ GET PROFILE
    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        """
        GET /api/user/profile/
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # ✅ UPDATE PROFILE (FIXED NAME)
    @action(detail=False, methods=['put', 'patch'], url_path='update-profile')
    def update_profile(self, request):
        """
        PUT /api/user/update-profile/
        """
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )

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

    # ✅ UPDATE LOCATION
    @action(detail=False, methods=['post'], url_path='location')
    def location(self, request):
        """
        POST /api/user/location/
        """
        serializer = LocationUpdateSerializer(data=request.data)

        if serializer.is_valid():
            request.user.latitude = serializer.validated_data.get('latitude')
            request.user.longitude = serializer.validated_data.get('longitude')
            request.user.location_name = serializer.validated_data.get('location_name')

            request.user.save()

            return Response(
                {
                    'message': 'Location updated successfully',
                    'user': UserSerializer(request.user).data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)