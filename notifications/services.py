"""
Firebase Cloud Messaging service.
"""
import logging
import json
from decouple import config

try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

logger = logging.getLogger(__name__)


class FCMService:
    """Service for Firebase Cloud Messaging."""

    def __init__(self):
        self.is_initialized = False
        self.firebase_credentials_path = config('FIREBASE_CREDENTIALS', default='')
        
        if FIREBASE_AVAILABLE and self.firebase_credentials_path:
            try:
                cred = credentials.Certificate(self.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                self.is_initialized = True
            except Exception as e:
                logger.error(f"Firebase initialization error: {str(e)}")

    def send_notification(self, token, title, body, data=None):
        """
        Send a push notification via FCM.
        
        Args:
            token (str): FCM device token
            title (str): Notification title
            body (str): Notification body
            data (dict): Additional data to send
            
        Returns:
            dict: Response with success status and message ID or error
        """
        if not self.is_initialized:
            return {
                'success': False,
                'error': 'Firebase is not initialized'
            }

        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                token=token,
            )
            
            response = messaging.send(message)
            
            logger.info(f"FCM notification sent successfully: {response}")
            return {
                'success': True,
                'message_id': response
            }
        except Exception as e:
            logger.error(f"FCM send error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_multicast_notification(self, tokens, title, body, data=None):
        """
        Send a push notification to multiple devices via FCM.
        
        Args:
            tokens (list): List of FCM device tokens
            title (str): Notification title
            body (str): Notification body
            data (dict): Additional data to send
            
        Returns:
            dict: Response with success status and statistics
        """
        if not self.is_initialized:
            return {
                'success': False,
                'error': 'Firebase is not initialized'
            }

        if not tokens:
            return {
                'success': False,
                'error': 'No tokens provided'
            }

        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                tokens=tokens,
            )
            
            response = messaging.send_multicast(message)
            
            logger.info(f"FCM multicast notification sent: {response.success_count} successful")
            return {
                'success': True,
                'successful': response.success_count,
                'failed': response.failure_count,
                'message_ids': [r.message_id for r in response.responses if hasattr(r, 'message_id')]
            }
        except Exception as e:
            logger.error(f"FCM multicast send error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# Singleton instance
fcm_service = FCMService()
