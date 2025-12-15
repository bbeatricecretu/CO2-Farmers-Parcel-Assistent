from typing import Optional, Tuple
import re

class IntentService:
    LIST_KEYWORDS = {"parcels", "fields"}
    DETAIL_KEYWORDS = {"detail", "details", "about", "information", "info"}
    ACTION_KEYWORDS = {"show", "list", "see", "get", "what", "tell"}
    
    @staticmethod
    def detect_intent(message: str) -> str:
        """Detect user intent from message text."""
        message_lower = message.lower()
        words = set(message_lower.split())
        
        # Check for parcel details (e.g., "show details for parcel P1")
        if (words & IntentService.DETAIL_KEYWORDS or "parcel" in message_lower) and IntentService._contains_parcel_id(message):
            return "PARCEL_DETAILS"
        
        # Check for list all parcels
        if words & IntentService.LIST_KEYWORDS and words & IntentService.ACTION_KEYWORDS:
            return "LIST_PARCELS"
        
        return "UNKNOWN"
    
    @staticmethod
    def _contains_parcel_id(message: str) -> bool:
        """Check if message contains a parcel ID pattern."""
        return bool(re.search(r'\bP\d+\b', message, re.IGNORECASE))
    
    @staticmethod
    def extract_parcel_id(message: str) -> Optional[str]:
        """Extract parcel ID from message (e.g., P1, P2)."""
        match = re.search(r'\b(P\d+)\b', message, re.IGNORECASE)
        return match.group(1).upper() if match else None
