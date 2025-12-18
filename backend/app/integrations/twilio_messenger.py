"""Twilio WhatsApp integration."""
try:
    from twilio.rest import Client
    from twilio.request_validator import RequestValidator
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None
    RequestValidator = None

from app.integrations.base_messenger import BaseMessenger
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class TwilioMessenger(BaseMessenger):
    """Twilio WhatsApp messaging implementation."""
    
    def __init__(self):
        """Initialize Twilio client with credentials from settings."""
        if not TWILIO_AVAILABLE:
            raise ValueError("Twilio SDK not installed. Run: pip install twilio")
            
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_PHONE_NUMBER
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError(
                "Twilio credentials not configured. "
                "Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
        self.validator = RequestValidator(self.auth_token)
        logger.info("Twilio messenger initialized successfully")
    
    def send_message(self, to: str, message: str) -> bool:
        """
        Send a WhatsApp message via Twilio.
        
        Args:
            to: Phone number (with or without 'whatsapp:' prefix)
            message: Text message to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            # Normalize phone number
            clean_phone = self.normalize_phone(to)
            
            # Twilio requires 'whatsapp:' prefix
            from_whatsapp = f'whatsapp:{self.from_number}'
            to_whatsapp = f'whatsapp:{clean_phone}'
            
            # Send message
            twilio_message = self.client.messages.create(
                from_=from_whatsapp,
                body=message,
                to=to_whatsapp
            )
            
            logger.info(f"Message sent successfully. SID: {twilio_message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message via Twilio: {e}")
            return False
    
    def validate_webhook(self, request_data: dict) -> bool:
        """
        Validate Twilio webhook signature.
        
        Args:
            request_data: Dictionary containing 'url', 'signature', and 'form_data'
            
        Returns:
            True if webhook signature is valid, False otherwise
        """
        try:
            url = request_data.get('url', '')
            signature = request_data.get('signature', '')
            form_data = request_data.get('form_data', {})
            
            is_valid = self.validator.validate(url, form_data, signature)
            
            if not is_valid:
                logger.warning("Invalid Twilio webhook signature")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error validating Twilio webhook: {e}")
            return False
