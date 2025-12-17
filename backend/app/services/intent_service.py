from typing import Optional
import re
from sqlalchemy.orm import Session
from app.ai.factory import get_intent_classifier
from app.services.farmer_service import FarmerService
from app.services.parcel_service import ParcelService
from app.services.report_service import ReportService

class IntentService:
    def __init__(self, db: Session = None):
        # db is optional to maintain backward compatibility if used statically, 
        # but required for full chat handling
        if db:
            self.farmer_service = FarmerService(db)
            self.parcel_service = ParcelService(db)
            self.report_service = ReportService(db)
    
    def handle_message(self, phone: str, text: str) -> str:
        """Handle incoming chat message and return appropriate response."""
        if not hasattr(self, 'farmer_service'):
            raise ValueError("IntentService must be initialized with a database session to handle messages.")
            
        farmer = self.farmer_service.get_by_phone(phone)
        
        #User not linked yet
        if not farmer:
            return "Welcome! Please type your username to link your account."
        
        # User is linked - detect intent
        intent = self.detect_intent(text)
        
        if intent == "LIST_PARCELS":
            return self.parcel_service.format_parcels_list(farmer)
        
        elif intent == "PARCEL_DETAILS":
            parcel_id = self.extract_parcel_id(text)
            if parcel_id:
                return self.parcel_service.get_parcel_details(parcel_id, farmer)
            else:
                return "Please specify a parcel ID (e.g., P1, P2)."
            
        elif intent == "PARCEL_STATUS":
            parcel_id = self.extract_parcel_id(text)
            if parcel_id:
                return self.parcel_service.get_parcel_status(parcel_id, farmer)
            else:
                return "Please specify a parcel ID (e.g., P1, P2)."
            
        elif intent == "SET_REPORT_FREQUENCY":
            frequency = self.extract_report_frequency(text)
            if frequency:
                return self.report_service.set_report_frequency(phone, frequency)
            else:
                return "Please specify a valid frequency (e.g., 'daily', 'weekly', or '2 days')."
            
        elif intent == "UNKNOWN":
                return (
                    "Sorry, I didn’t understand your request.\n\n"
                    "Here are some things you can ask me:\n"
                    "- Show my parcels\n"
                    "- Check the status of a parcel\n"
                    "- Get details about a parcel\n"
                    "- Change how often I receive reports"
                )
        else:
            return f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."

    @staticmethod
    def detect_intent(message: str) -> str:
        """Detect user intent from message text."""
        classifier = get_intent_classifier()
        return classifier.classify(message)
    

    
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
