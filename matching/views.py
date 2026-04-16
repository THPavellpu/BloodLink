"""
Views for donor matching.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import find_matching_donors
from .serializers import DonorMatchSerializer, BloodMatchQuerySerializer


class DonorMatchingViewSet(viewsets.ViewSet):
    """
    ViewSet for donor matching operations.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def match(self, request):
        """
        Find matching donors for a blood request.
        
        GET /api/donors/match/?blood_group=A+&latitude=40.7128&longitude=-74.0060&limit=50
        """
        # Get query parameters
        blood_group = request.query_params.get('blood_group')
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        limit = request.query_params.get('limit', 50)

        # Validate parameters
        if not all([blood_group, latitude, longitude]):
            return Response(
                {'error': 'Missing required parameters: blood_group, latitude, longitude'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            limit = int(limit)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid parameter types. latitude and longitude must be floats, limit must be int.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate ranges
        if not (-90 <= latitude <= 90):
            return Response(
                {'error': 'Latitude must be between -90 and 90'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not (-180 <= longitude <= 180):
            return Response(
                {'error': 'Longitude must be between -180 and 180'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not (1 <= limit <= 200):
            return Response(
                {'error': 'Limit must be between 1 and 200'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find matching donors
        matched_donors = find_matching_donors(
            blood_group, latitude, longitude, limit
        )

        # Serialize response
        serializer = DonorMatchSerializer(matched_donors, many=True)
        return Response({
            'blood_group': blood_group,
            'request_location': {
                'latitude': latitude,
                'longitude': longitude
            },
            'total_matches': len(matched_donors),
            'donors': serializer.data
        })
