from sqlalchemy.orm import Session
from app.models.database import Farmer
from app.services.intent_service import IntentService
from app.services.farmer_service import FarmerService
from app.services.parcel_service import ParcelService
from app.services.report_service import ReportService

class ChatService:
    def __init__(self, db: Session):
        self.intent_service = IntentService()
        self.farmer_service = FarmerService(db)
        self.parcel_service = ParcelService(db)
        self.report_service = ReportService(db)
    
    def handle_message(self, phone: str, text: str) -> str:
        """Handle incoming chat message and return appropriate response."""
        farmer = self.farmer_service.get_by_phone(phone)
        
        if not farmer:
            return "Welcome! Please type your username to link your account."
        
        # User is linked - detect intent
        intent = self.intent_service.detect_intent(text)
        
        if intent == "LIST_PARCELS":
            return self.parcel_service.format_parcels_list(farmer)
        elif intent == "PARCEL_DETAILS":
            parcel_id = self.intent_service.extract_parcel_id(text)
            if parcel_id:
                return self.parcel_service.get_parcel_details(parcel_id, farmer)
            else:
                return "Please specify a parcel ID (e.g., P1, P2)."
        elif intent == "PARCEL_STATUS":
            parcel_id = self.intent_service.extract_parcel_id(text)
            if parcel_id:
                return self.parcel_service.get_parcel_status(parcel_id, farmer)
            else:
                return "Please specify a parcel ID (e.g., P1, P2)."
        elif intent == "SET_REPORT_FREQUENCY":
            frequency = self.intent_service.extract_report_frequency(text)
            if frequency:
                return self.report_service.set_report_frequency(phone, frequency)
            else:
                return "Please specify a valid frequency (e.g., 'daily', 'weekly', or '2 days')."
        else:
            return f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."
