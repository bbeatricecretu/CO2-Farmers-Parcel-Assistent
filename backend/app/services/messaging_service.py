"""Messaging service factory for selecting messaging provider."""
from app.integrations.base_messenger import BaseMessenger
from app.integrations.twilio_messenger import TwilioMessenger
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class MockMessenger(BaseMessenger):
    """Mock messenger for testing without real API calls."""
    
    def __init__(self):
        """Initialize mock messenger."""
        self.sent_messages = []
        logger.info("Mock messenger initialized (no real messages will be sent)")
    
    def send_message(self, to: str, message: str) -> bool:
        """Store message instead of sending."""
        clean_phone = self.normalize_phone(to)
        self.sent_messages.append({
            'to': clean_phone,
            'message': message
        })
        logger.info(f"Mock: Would send message to {clean_phone}")
        return True
    
    def validate_webhook(self, request_data: dict) -> bool:
        """Always return True for mock validation."""
        return True


def get_messenger() -> BaseMessenger:
    """
    Factory function to get the appropriate messenger based on configuration.
    
    Returns:
        BaseMessenger: Instance of the configured messaging provider
        
    Raises:
        ValueError: If provider is not supported
    """
    provider = settings.MESSAGING_PROVIDER.lower()
    
    if provider == "twilio":
        try:
            return TwilioMessenger()
        except ValueError as e:
            logger.warning(f"Twilio initialization failed: {e}. Falling back to mock messenger.")
            return MockMessenger()
    
    elif provider == "mock":
        return MockMessenger()
    
    else:
        raise ValueError(
            f"Unsupported messaging provider: {provider}. "
            f"Supported providers: 'twilio', 'mock'"
        )
