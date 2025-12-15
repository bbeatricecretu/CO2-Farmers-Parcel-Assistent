from sqlalchemy.orm import Session
from app.models.base import Farmer, Parcel
from app.repositories.parcel_repo import ParcelRepository
from app.services.index_service import IndexInterpretationService

class ParcelService:
    def __init__(self, db: Session):
        self.parcel_repo = ParcelRepository(db)
        self.index_interpreter = IndexInterpretationService()
    
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
    
    def get_parcel_details(self, parcel_id: str, farmer: Farmer) -> str:
        """Get detailed information about a specific parcel including latest indices."""
        parcel = self.parcel_repo.get_by_id(parcel_id)
        
        if not parcel:
            return f"Parcel {parcel_id} not found."
        
        # Check if parcel belongs to the farmer
        if parcel.farmer_id != farmer.id:
            return f"Parcel {parcel_id} does not belong to you."
        
        # Get latest indices
        indices = sorted(parcel.indices, key=lambda x: x.date, reverse=True)
        
        details = f"**Parcel {parcel.id}: {parcel.name}**\n\n"
        details += f"📏 Area: {parcel.area_ha} ha\n"
        details += f"🌾 Crop: {parcel.crop}\n"
        
        if indices:
            latest = indices[0]
            details += f"\n**Latest Indices ({latest.date}):**\n"
            details += "\n*Vegetation:*\n"
            if latest.ndvi is not None:
                details += f"  • NDVI: {latest.ndvi:.2f}\n"
            if latest.ndmi is not None:
                details += f"  • NDMI: {latest.ndmi:.2f}\n"
            if latest.ndwi is not None:
                details += f"  • NDWI: {latest.ndwi:.2f}\n"
            
            details += "\n*Soil:*\n"
            if latest.soc is not None:
                details += f"  • SOC: {latest.soc:.2f}\n"
            if latest.nitrogen is not None:
                details += f"  • Nitrogen: {latest.nitrogen:.2f}\n"
            if latest.phosphorus is not None:
                details += f"  • Phosphorus: {latest.phosphorus:.2f}\n"
            if latest.potassium is not None:
                details += f"  • Potassium: {latest.potassium:.2f}\n"
            if latest.ph is not None:
                details += f"  • pH: {latest.ph:.2f}\n"
        else:
            details += "\n⚠️ No indices data available for this parcel.\n"
        
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
        
        # Generate status summary
        summary = f"**Status Summary for Parcel {parcel.id}: {parcel.name}**\n"
        summary += f"({parcel.area_ha} ha, {parcel.crop})\n"
        summary += f"Data from: {latest.date}\n\n"
        
        # Vegetation status
        if latest.ndvi is not None:
            summary += f"🌱 **Vegetation (NDVI: {latest.ndvi:.2f}):** {self.index_interpreter.ndvi_status(latest.ndvi)}\n\n"
        
        # Moisture status
        if latest.ndmi is not None:
            summary += f"💧 **Moisture (NDMI: {latest.ndmi:.2f}):** {self.index_interpreter.ndmi_status(latest.ndmi)}\n\n"
        
        # Water status
        if latest.ndwi is not None:
            summary += f"💦 **Water (NDWI: {latest.ndwi:.2f}):** {self.index_interpreter.ndwi_status(latest.ndwi)}\n\n"
        
        # Soil organic carbon
        if latest.soc is not None:
            summary += f"🌾 **Soil Organic Carbon (SOC: {latest.soc:.2f}):** {self.index_interpreter.soc_status(latest.soc)}\n\n"
        
        # Nitrogen
        if latest.nitrogen is not None:
            summary += f"🧪 **Nitrogen (N: {latest.nitrogen:.2f}):** {self.index_interpreter.nitrogen_status(latest.nitrogen)}\n\n"
        
        # Phosphorus
        if latest.phosphorus is not None:
            summary += f"🧪 **Phosphorus (P: {latest.phosphorus:.2f}):** {self.index_interpreter.phosphorus_status(latest.phosphorus)}\n\n"
        
        # Potassium
        if latest.potassium is not None:
            summary += f"🧪 **Potassium (K: {latest.potassium:.2f}):** {self.index_interpreter.potassium_status(latest.potassium)}\n\n"
        
        # pH
        if latest.ph is not None:
            summary += f"⚗️ **pH Level ({latest.ph:.2f}):** {self.index_interpreter.ph_status(latest.ph)}\n"
        
        return summary
