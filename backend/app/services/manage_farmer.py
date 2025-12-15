from sqlalchemy.orm import Session
from app.repositories.farmer_repo import FarmerRepository

class ManageFarmerService:
    def __init__(self, db: Session):
        self.farmer_repo = FarmerRepository(db)
    
    def get_all_farmers(self):
        return self.farmer_repo.get_all()
    
    def get_farmer(self, farmer_id: str):
        return self.farmer_repo.get_by_id(farmer_id)
