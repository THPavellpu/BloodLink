"""
Views for notification management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import NotificationToken
from .serializers import NotificationTokenSerializer, FCMTokenRegisterSerializer


class NotificationViewSet(viewsets.ViewSet):
    """
    ViewSet for notification operations.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def register_token(self, request):
        """
        Register or update FCM token for the current user.
        
        POST /api/notifications/register_token/
        
        Request body:
        {
            "token": "fcm_device_token_here"
        }
        """
        serializer = FCMTokenRegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        token = serializer.validated_data['token']

        # Update or create notification token
        notification_token, created = NotificationToken.objects.update_or_create(
            user=request.user,
            defaults={'token': token}
        )

        token_serializer = NotificationTokenSerializer(notification_token)
        action_msg = 'Token registered' if created else 'Token updated'
        
        return Response(
            {
                'message': action_msg,
                'token': token_serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_token(self, request):
        """
        Get current user's FCM token.
        
        GET /api/notifications/my_token/
        """
        try:
            token = request.user.fcm_token
            serializer = NotificationTokenSerializer(token)
            return Response(serializer.data)
        except NotificationToken.DoesNotExist:
            return Response(
                {'message': 'No FCM token registered for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['delete'])
    def deregister_token(self, request):
        """
        Deregister FCM token for the current user.
        
        DELETE /api/notifications/deregister_token/
        """
        try:
            request.user.fcm_token.delete()
            return Response(
                {'message': 'FCM token deregistered successfully'},
                status=status.HTTP_200_OK
            )
        except NotificationToken.DoesNotExist:
            return Response(
                {'message': 'No FCM token found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
