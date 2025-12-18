"""Abstract base class for messaging providers."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseMessenger(ABC):
    """Abstract interface for messaging providers (Twilio, Meta WhatsApp, etc.)."""
    
    @abstractmethod
    def send_message(self, to: str, message: str) -> bool:
        """
        Send a message to a phone number.
        
        Args:
            to: Phone number in E.164 format (e.g., "+40741111111")
            message: Text message to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_webhook(self, request_data: dict) -> bool:
        """
        Validate that incoming webhook is authentic.
        
        Args:
            request_data: Raw request data from webhook
            
        Returns:
            True if webhook is valid, False otherwise
        """
        pass
    
    def normalize_phone(self, phone: str) -> str:
        """
        Normalize phone number by removing 'whatsapp:' prefix if present.
        
        Args:
            phone: Phone number (may have 'whatsapp:' prefix)
            
        Returns:
            Clean phone number in E.164 format
        """
        if phone.startswith('whatsapp:'):
            return phone.replace('whatsapp:', '')
        return phone
