from sqlalchemy.orm import Session
from app.models.base import Farmer
from app.repositories.parcel_repo import ParcelRepository
from app.services.index_service import IndexInterpretationService
from app.ai.factory import get_summary_generator

class ParcelService:
    def __init__(self, db: Session):
        self.parcel_repo = ParcelRepository(db)
        self.index_interpreter = IndexInterpretationService()
        self.summary_generator = get_summary_generator()
    
    def get_all_parcels(self):
        """Get all parcels."""
        return self.parcel_repo.get_all()
    
    def get_farmer_parcels(self, farmer_id: str):
        """Get parcels by farmer ID."""
        return self.parcel_repo.get_by_farmer_id(farmer_id)
    
    def format_parcels_list(self, farmer: Farmer) -> dict:
        """Format farmer's parcels into a structured list."""
        parcels = farmer.parcels
        
        return {
            "parcels": [
                {
                    "id": p.id,
                    "name": p.name,
                    "area": float(p.area_ha),
                    "crop": p.crop
                }
                for p in parcels
            ]
        }
    
    def get_parcel_details(self, parcel_id: str, farmer: Farmer):
        """Get detailed information about a specific parcel including latest indices."""
        parcel = self.parcel_repo.get_by_id(parcel_id)
        
        if not parcel:
            return {"error": f"Parcel {parcel_id} not found."}
        
        # Check if parcel belongs to the farmer
        if parcel.farmer_id != farmer.id:
            return {"error": f"Parcel {parcel_id} does not belong to you."}
        
        # Get latest indices
        indices = sorted(parcel.indices, key=lambda x: x.date, reverse=True)
        
        details = {
            "parcel_id": parcel.id,
            "name": parcel.name,
            "area_ha": float(parcel.area_ha),
            "crop": parcel.crop,
            "data_date": None,
            "indices": None
        }
        
        if indices:
            latest = indices[0]
            details["data_date"] = str(latest.date)
            details["indices"] = {
                "ndvi": round(float(latest.ndvi), 2) if latest.ndvi is not None else None,
                "ndmi": round(float(latest.ndmi), 2) if latest.ndmi is not None else None,
                "ndwi": round(float(latest.ndwi), 2) if latest.ndwi is not None else None,
                "soc": round(float(latest.soc), 2) if latest.soc is not None else None,
                "nitrogen": round(float(latest.nitrogen), 2) if latest.nitrogen is not None else None,
                "phosphorus": round(float(latest.phosphorus), 2) if latest.phosphorus is not None else None,
                "potassium": round(float(latest.potassium), 2) if latest.potassium is not None else None,
                "ph": round(float(latest.ph), 2) if latest.ph is not None else None
            }
        
        return details
    
    def get_parcel_status(self, parcel_id: str, farmer: Farmer) -> str:
        """Get rule-based status summary for a specific parcel."""
        parcel = self.parcel_repo.get_by_id(parcel_id)
        
        if not parcel:
            return f"Parcel {parcel_id} not found."
        
        # Check if parcel belongs to the farmer
        if parcel.farmer_id != farmer.id:
            return f"Parcel {parcel_id} does not belong to you."
        
        # Get latest indices
        indices = sorted(parcel.indices, key=lambda x: x.date, reverse=True)
        
        if not indices:
            return f"No data available for parcel {parcel.id} ({parcel.name})."
        
        latest = indices[0]
        
        # Prepare data for summary generation
        indices_data = {
            "latest_index": latest,
            "parcel_name": parcel.name,
            "area_ha": parcel.area_ha,
            "crop": parcel.crop
        }
        
        # Generate summary using the configured strategy (AI or Rule-Based)
        return self.summary_generator.generate_parcel_summary(parcel.id, indices_data)
