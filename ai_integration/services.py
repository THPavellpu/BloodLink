"""
Gemini AI integration service.
"""
import logging
from decouple import config

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiAIService:
    """Service for Gemini AI interactions."""

    def __init__(self):
        self.api_key = config('GEMINI_API_KEY', default='')
        self.model_name = 'gemini-pro'
        
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)

    def is_configured(self):
        """Check if Gemini AI is properly configured."""
        return GEMINI_AVAILABLE and bool(self.api_key)

    def generate_response(self, question, context=None):
        """
        Generate a response using Gemini AI.
        
        Args:
            question (str): The user's question
            context (str): Optional context about blood donation
            
        Returns:
            dict: Response containing the generated answer or error
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Gemini AI is not configured. Please set GEMINI_API_KEY.'
            }

        try:
            # Create a prompt with blood donation context if provided
            if context:
                prompt = f"""You are a helpful assistant about blood donation and medical information.
Context: {context}

User Question: {question}

Please provide a helpful and accurate response."""
            else:
                prompt = f"""You are a helpful assistant about blood donation and medical information.

User Question: {question}

Please provide a helpful and accurate response."""

            # Generate content using Gemini
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)

            return {
                'success': True,
                'answer': response.text,
                'model': self.model_name
            }

        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to generate response: {str(e)}'
            }


# Singleton instance
gemini_service = GeminiAIService()
