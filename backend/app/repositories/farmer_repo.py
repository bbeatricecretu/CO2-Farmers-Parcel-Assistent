from sqlalchemy.orm import Session
from app.models.database import Farmer

class FarmerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Farmer).all()
    
    def get_by_id(self, farmer_id: str):
        return self.db.query(Farmer).filter(Farmer.id == farmer_id).first()
    
    
 