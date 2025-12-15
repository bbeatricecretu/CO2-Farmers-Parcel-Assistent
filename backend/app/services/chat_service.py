from sqlalchemy.orm import Session
from app.models.database import Farmer
from app.services.intent_service import IntentService
from app.services.farmer_service import FarmerService
from app.services.parcel_service import ParcelService

class ChatService:
    def __init__(self, db: Session):
        self.intent_service = IntentService()
        self.farmer_service = FarmerService(db)
        self.parcel_service = ParcelService(db)
    
    def handle_message(self, phone: str, text: str) -> str:
        """Handle incoming chat message and return appropriate response."""
        farmer = self.farmer_service.get_by_phone(phone)
        
        if not farmer:
            return "Welcome! Please type your username to link your account."
        
        # User is linked - detect intent
        intent = self.intent_service.detect_intent(text)
        
        if intent == "LIST_PARCELS":
            return self.parcel_service.format_parcels_list(farmer)
        else:
            return f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."
