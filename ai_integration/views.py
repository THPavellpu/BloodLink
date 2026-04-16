"""
Views for AI integration.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import gemini_service
from .serializers import AIQuerySerializer, AIResponseSerializer


class AIIntegrationViewSet(viewsets.ViewSet):
    """
    ViewSet for AI chat operations.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Chat with Gemini AI for blood donation related questions.
        
        POST /api/ai/chat/
        
        Request body:
        {
            "question": "What is blood type O+?",
            "context": "I want to know about blood donation" (optional)
        }
        """
        serializer = AIQuerySerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question = serializer.validated_data['question']
        context = serializer.validated_data.get('context', '')

        # Get AI response
        response = gemini_service.generate_response(question, context)

        # Serialize response
        response_serializer = AIResponseSerializer(response)
        
        if response.get('success'):
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                response_serializer.data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
