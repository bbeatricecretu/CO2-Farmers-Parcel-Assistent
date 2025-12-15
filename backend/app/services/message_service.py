from sqlalchemy.orm import Session
from app.models.database import Farmer
from app.repositories.farmer_repo import FarmerRepository
from app.repositories.parcel_repo import ParcelRepository
from app.services.intent_service import IntentService

class MessageService:
    def __init__(self, db: Session):
        self.db = db
        self.farmer_repo = FarmerRepository(db)
        self.parcel_repo = ParcelRepository(db)
        self.intent_service = IntentService()
    
    def handle_message(self, phone: str, text: str) -> str:
        """Handle incoming message and return appropriate response."""
        farmer = self.farmer_repo.get_by_phone(phone)
        
        if not farmer:
            return "Welcome! Please type your username to link your account."
        
        # User is linked - detect intent
        intent = self.intent_service.detect_intent(text)
        
        if intent == "LIST_PARCELS":
            return self._handle_list_parcels(farmer)
        else:
            return f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."
    
    def _handle_list_parcels(self, farmer: Farmer) -> str:
        """Handle list parcels request."""
        parcels = farmer.parcels
        
        if parcels:
            parcel_list = "\n".join([
                f"- {p.id}: {p.name} ({p.area_ha} ha, {p.crop})"
                for p in parcels
            ])
            return f"Your parcels:\n{parcel_list}"
        else:
            return "You don't have any parcels registered."
    
    def link_account(self, phone: str, username: str) -> str:
        """Link a phone number to a farmer account."""
        farmer = self.farmer_repo.get_by_username(username)
        
        if not farmer:
            return "Username not found. Please try again with a valid username."
        
        if farmer.phone:
            return "This account is already linked. Please try again with a different username."
        
        # Link the account
        farmer.phone = phone
        self.db.commit()
        return f"Great, your account has been linked to {phone}. You can now ask about your parcels."
