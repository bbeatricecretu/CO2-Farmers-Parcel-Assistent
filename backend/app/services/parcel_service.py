from sqlalchemy.orm import Session
from app.models.database import Farmer
from app.repositories.parcel_repo import ParcelRepository

class ParcelService:
    def __init__(self, db: Session):
        self.parcel_repo = ParcelRepository(db)
    
    def get_all_parcels(self):
        """Get all parcels."""
        return self.parcel_repo.get_all()
    
    def get_farmer_parcels(self, farmer_id: str):
        """Get parcels by farmer ID."""
        return self.parcel_repo.get_by_farmer_id(farmer_id)
    
    def format_parcels_list(self, farmer: Farmer) -> str:
        """Format farmer's parcels into a readable list."""
        parcels = farmer.parcels
        
        if parcels:
            parcel_list = "\n".join([
                f"- {p.id}: {p.name} ({p.area_ha} ha, {p.crop})"
                for p in parcels
            ])
            return f"Your parcels:\n{parcel_list}"
        else:
            return "You don't have any parcels registered."
