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
        # Ensure we have fresh data from the database
        self.farmer_repo.refresh_session()
        
        # Check if phone is already linked to another account
        existing_farmer_with_phone = self.farmer_repo.get_by_phone(phone)
        if existing_farmer_with_phone:
            if existing_farmer_with_phone.username == username:
                return f"Your account is already linked to this phone number."
            return f"This phone number is already linked to account '{existing_farmer_with_phone.username}'."
        
        # Get farmer by username
        farmer = self.farmer_repo.get_by_username(username)
        
        if not farmer:
            return "Username not found. Please try again with a valid username."
        
        if farmer.phone:
            return "This account is already linked. Please try again with a different username."
        
        # Link the account
        self.farmer_repo.link_phone_to_farmer(farmer, phone)
        return f"Great, your account has been linked to {phone}. You can now ask about your parcels."
