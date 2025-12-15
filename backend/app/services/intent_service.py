from typing import Optional, Tuple
import re

class IntentService:
    LIST_KEYWORDS = {"parcels", "fields"}
    DETAIL_KEYWORDS = {"detail", "details", "about", "information", "info"}
    STATUS_KEYWORDS = {"how", "status", "summary", "condition", "health"}
    SET_KEYWORDS = {"set", "make", "change", "update"}
    REPORT_KEYWORDS = {"report", "reports", "frequency"}
    ACTION_KEYWORDS = {"show", "list", "see", "get", "what", "tell", "give"}
    
    @staticmethod
    def detect_intent(message: str) -> str:
        """Detect user intent from message text."""
        message_lower = message.lower()
        words = set(message_lower.split())
        
        # Check for setting report frequency (e.g., "Set my report frequency to daily")
        if (words & IntentService.SET_KEYWORDS) and (words & IntentService.REPORT_KEYWORDS or "frequency" in message_lower):
            return "SET_REPORT_FREQUENCY"
        
        # Check for parcel status/summary (e.g., "How is parcel P1?", "What's the status of P1?")
        if (words & IntentService.STATUS_KEYWORDS) and IntentService._contains_parcel_id(message):
            return "PARCEL_STATUS"
        
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
    
    @staticmethod
    def extract_report_frequency(message: str) -> Optional[str]:
        """Extract report frequency from message (e.g., daily, weekly, 2 days)."""
        message_lower = message.lower()
        
        # Check for daily
        if "daily" in message_lower or "every day" in message_lower:
            return "daily"
        
        # Check for weekly
        if "weekly" in message_lower or "every week" in message_lower or "week" in message_lower:
            return "weekly"
        
        # Check for custom frequency like "2 days", "3 days", "every 2 days"
        match = re.search(r'(?:every\s+)?(\d+)\s+days?', message_lower)
        if match:
            return f"{match.group(1)} days"
        
        return None
