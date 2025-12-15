from sqlalchemy.orm import Session
from app.repositories.farmer_repo import FarmerRepository

class FarmerService:
    def __init__(self, db: Session):
        self.farmer_repo = FarmerRepository(db)
    
    def get_by_phone(self, phone: str):
        """Get farmer by phone number."""
        return self.farmer_repo.get_by_phone(phone)
    
    def get_by_username(self, username: str):
        """Get farmer by username."""
        return self.farmer_repo.get_by_username(username)
    
    def link_account(self, phone: str, username: str) -> str:
        """Link a phone number to a farmer account."""
        farmer = self.farmer_repo.get_by_username(username)
        
        if not farmer:
            return "Username not found. Please try again with a valid username."
        
        if farmer.phone:
            return "This account is already linked. Please try again with a different username."
        
        # Link the account
        self.farmer_repo.link_phone_to_farmer(farmer, phone)
        return f"Great, your account has been linked to {phone}. You can now ask about your parcels."
