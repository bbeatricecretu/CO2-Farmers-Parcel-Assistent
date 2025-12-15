from sqlalchemy.orm import Session
from app.repositories.parcel_repo import ParcelRepository

class ParcelService:
    def __init__(self, db: Session):
        self.parcel_repo = ParcelRepository(db)
    
    def get_all_parcels(self):
        return self.parcel_repo.get_all()
    
    def get_farmer_parcels(self, farmer_id: str):
        return self.parcel_repo.get_by_farmer_id(farmer_id)
