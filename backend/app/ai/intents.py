"""Intent classification strategies."""
from typing import Protocol
from app.ai.prompts import get_intent_classification_prompt
import re

class IntentClassifier(Protocol):
    """Protocol for intent classification strategies."""
    
    def classify(self, message: str) -> str:
        """Classify the intent of a user message."""
        ...

class RuleBasedIntentClassifier:
    """Classify intent using keyword matching rules."""
    
    # sets - fast membership checks
    LIST_KEYWORDS = {"parcels", "fields"}
    DETAIL_KEYWORDS = {"detail", "details", "about", "information", "info"}
    STATUS_KEYWORDS = {"how", "status", "summary", "condition", "health"}
    SET_KEYWORDS = {"set", "make", "change", "update"}
    REPORT_KEYWORDS = {"report", "reports", "frequency"}
    ACTION_KEYWORDS = {"show", "list", "see", "get", "what", "tell", "give"}
    
    def classify(self, message: str) -> str:
        """Detect intent using rule-based approach."""
        message_lower = message.lower()
        words = set(message_lower.split())
        
        # Helper for parcel ID check
        has_parcel_id = bool(re.search(r'\bP\d+\b', message, re.IGNORECASE))
        
        # 4. Check for setting report frequency (e.g., "Set my report frequency to daily")
        if (words & self.SET_KEYWORDS) and (words & self.REPORT_KEYWORDS or "frequency" in message_lower):
            return "SET_REPORT_FREQUENCY"
            
        # 3. Check for parcel status/summary (e.g., "How is parcel P1?", "What's the status of P1?")
        if (words & self.STATUS_KEYWORDS) and has_parcel_id:
            return "PARCEL_STATUS"
            
        # 2. Check for parcel details (e.g., "show details for parcel P1")
        if (words & self.DETAIL_KEYWORDS or "parcel" in message_lower) and has_parcel_id:
            return "PARCEL_DETAILS"
            
        # 1. Check for list all parcels
        if words & self.LIST_KEYWORDS and words & self.ACTION_KEYWORDS:
            return "LIST_PARCELS"
        
        return "UNKNOWN"

class LLMIntentClassifier:
    """Classify intent using an LLM."""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def classify(self, message: str) -> str:
        """Detect intent using LLM."""
        prompt = get_intent_classification_prompt(message)
        
        try:
            result = self.llm_client.generate(prompt).strip().upper()
            
            # Validate result
            valid_intents = {"LIST_PARCELS", "PARCEL_DETAILS", "PARCEL_STATUS", "SET_REPORT_FREQUENCY", "UNKNOWN"}
            if result in valid_intents:
                return result
            return "UNKNOWN"
            
        except Exception as e:
            print(f"LLM intent detection failed: {e}. Falling back to rule-based.")
            rule_based = RuleBasedIntentClassifier()
            return rule_based.classify(message)
