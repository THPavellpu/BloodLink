"""
Views for blood requests.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import BloodRequest
from .serializers import (
    BloodRequestSerializer, BloodRequestCreateSerializer,
    BloodRequestUpdateSerializer
)


class BloodRequestViewSet(viewsets.ViewSet):
    """
    ViewSet for blood request operations.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_request(self, request):
        """
        Create a new blood request.
        
        POST /api/request/create/
        """
        serializer = BloodRequestCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            blood_request = serializer.save()
            return Response(
                {
                    'message': 'Blood request created successfully',
                    'request': BloodRequestSerializer(blood_request).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def all(self, request):
        """
        Get all blood requests (active/non-fulfilled).
        
        GET /api/request/all/
        """
        requests = BloodRequest.objects.filter(is_fulfilled=False).order_by('-created_at')
        serializer = BloodRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """
        Get current user's blood requests.
        
        GET /api/request/my_requests/
        """
        user_requests = BloodRequest.objects.filter(user=request.user)
        serializer = BloodRequestSerializer(user_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_by_id(self, request, pk=None):
        """
        Get a specific blood request by ID.
        
        GET /api/request/{id}/
        """
        blood_request = get_object_or_404(BloodRequest, id=pk)
        serializer = BloodRequestSerializer(blood_request)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'])
    def update_request(self, request, pk=None):
        """
        Update a blood request (only by owner).
        
        PUT /api/request/{id}/update_request/
        """
        blood_request = get_object_or_404(BloodRequest, id=pk)
        
        # Check if user owns this request
        if blood_request.user != request.user:
            return Response(
                {'error': 'You can only update your own requests'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BloodRequestUpdateSerializer(
            blood_request,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Blood request updated successfully',
                    'request': BloodRequestSerializer(blood_request).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def cancel(self, request, pk=None):
        """
        Cancel a blood request (only by owner).
        
        DELETE /api/request/{id}/cancel/
        """
        blood_request = get_object_or_404(BloodRequest, id=pk)
        
        # Check if user owns this request
        if blood_request.user != request.user:
            return Response(
                {'error': 'You can only cancel your own requests'},
                status=status.HTTP_403_FORBIDDEN
            )

        blood_request.delete()
        return Response(
            {'message': 'Blood request cancelled'},
            status=status.HTTP_204_NO_CONTENT
        )
