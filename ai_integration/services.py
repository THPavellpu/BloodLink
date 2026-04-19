import os
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiAIService:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = 'gemini-2.5-flash'  # You can change this to the desired Gemini model

        if not self.api_key:
            logger.error("❌ GEMINI_API_KEY NOT FOUND")
        else:
            logger.info("✅ GEMINI_API_KEY LOADED")

        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)

    def is_configured(self):
        return GEMINI_AVAILABLE and bool(self.api_key)

    def generate_response(self, question, context=None):

        if not self.is_configured():
            return {
                'success': False,
                'error': 'Gemini AI is not configured. Please set GEMINI_API_KEY.'
            }

        try:
            if context:
                prompt = f"""
You are a helpful assistant about blood donation.

Context: {context}
Question: {question}
"""
            else:
                prompt = f"""
You are a helpful assistant about blood donation.

Question: {question}
"""

            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)

            return {
                'success': True,
                'answer': response.text
            }

        except Exception as e:
            logger.error(f"Gemini AI error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


gemini_service = GeminiAIService()