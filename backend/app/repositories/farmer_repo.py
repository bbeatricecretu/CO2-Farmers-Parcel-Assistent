from sqlalchemy.orm import Session
from app.models.base import Farmer

class FarmerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Farmer).all()
    
    def get_by_id(self, farmer_id: str):
        return self.db.query(Farmer).filter(Farmer.id == farmer_id).first()
    
    def get_by_phone(self, phone: str):
        return self.db.query(Farmer).filter(Farmer.phone == phone).first()
    
    def get_by_username(self, username: str):
        return self.db.query(Farmer).filter(Farmer.username == username).first()
    
    def link_phone_to_farmer(self, farmer: Farmer, phone: str):
        """Link a phone number to a farmer account."""
        farmer.phone = phone
        self.db.commit()
        self.db.refresh(farmer)
        return farmer
    
    def refresh_session(self):
        """Expire all cached instances to ensure fresh data from database."""
        self.db.expire_all()