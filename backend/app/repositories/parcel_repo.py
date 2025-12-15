from sqlalchemy.orm import Session
from app.models.database import Parcel

class ParcelRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Parcel).all()
    
    def get_by_farmer_id(self, farmer_id: str):
        return self.db.query(Parcel).filter(Parcel.farmer_id == farmer_id).all()
    
    def get_by_id(self, parcel_id: str):
        """Get parcel by ID."""
        return self.db.query(Parcel).filter(Parcel.id == parcel_id).first()
