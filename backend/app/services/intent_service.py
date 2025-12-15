from typing import Optional

class IntentService:
    LIST_KEYWORDS = {"parcel", "parcels", "field", "fields"}
    ACTION_KEYWORDS = {"show", "list", "see", "get", "what"}
    
    @staticmethod
    def detect_intent(message: str) -> str:
        """Detect user intent from message text."""
        words = set(message.lower().split())
        
        if words & IntentService.LIST_KEYWORDS and words & IntentService.ACTION_KEYWORDS:
            return "LIST_PARCELS"
        
        return "UNKNOWN"
