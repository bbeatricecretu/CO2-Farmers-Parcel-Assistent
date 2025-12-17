from typing import Optional, Tuple
import re
import os

class IntentService:
    # sets - fast membership checks
    LIST_KEYWORDS = {"parcels", "fields"}
    DETAIL_KEYWORDS = {"detail", "details", "about", "information", "info"}
    STATUS_KEYWORDS = {"how", "status", "summary", "condition", "health"}
    SET_KEYWORDS = {"set", "make", "change", "update"}
    REPORT_KEYWORDS = {"report", "reports", "frequency"}
    ACTION_KEYWORDS = {"show", "list", "see", "get", "what", "tell", "give"}
    
    @staticmethod
    def detect_intent(message: str) -> str:
        """Detect user intent from message text."""
        from app.config import settings
        
        # Check if LLM is enabled
        use_llm = str(settings.USE_LLM).lower() == "true"
        
        if use_llm:
            api_key = settings.LLM_API_KEY
            if api_key:
                try:
                    return IntentService._detect_intent_with_llm(message, api_key)
                except Exception as e:
                    print(f"LLM intent detection failed: {e}. Falling back to rule-based.")
        
        # Rule-based intent detection (fallback or default)
        return IntentService._detect_intent_rule_based(message)
    
    @staticmethod
    def _detect_intent_with_llm(message: str, api_key: str) -> str:
        """Detect intent using LLM."""
        from app.ai.gemini_client import GeminiClient
        from app.ai.prompts import get_intent_classification_prompt
        
        client = GeminiClient(api_key)
        prompt = get_intent_classification_prompt(message)
        result = client.generate(prompt).strip().upper()
        
        # Validate result
        valid_intents = {"LIST_PARCELS", "PARCEL_DETAILS", "PARCEL_STATUS", "SET_REPORT_FREQUENCY", "UNKNOWN"}
        if result in valid_intents:
            return result
        return "UNKNOWN"
    
    @staticmethod
    def _detect_intent_rule_based(message: str) -> str:
        """Detect intent using rule-based approach."""
        message_lower = message.lower()
        words = set(message_lower.split()) 
        
        # & - intersection for sets

        # 4. Check for setting report frequency (e.g., "Set my report frequency to daily")
        if (words & IntentService.SET_KEYWORDS) and (words & IntentService.REPORT_KEYWORDS or "frequency" in message_lower):
            return "SET_REPORT_FREQUENCY"
        
        # 3. Check for parcel status/summary (e.g., "How is parcel P1?", "What's the status of P1?")
        if (words & IntentService.STATUS_KEYWORDS) and IntentService._contains_parcel_id(message):
            return "PARCEL_STATUS"
        
        # 2. Check for parcel details (e.g., "show details for parcel P1")
        if (words & IntentService.DETAIL_KEYWORDS or "parcel" in message_lower) and IntentService._contains_parcel_id(message):
            return "PARCEL_DETAILS"
        
        # 1. Check for list all parcels
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
