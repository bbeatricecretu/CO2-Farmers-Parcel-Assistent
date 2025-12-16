from sqlalchemy.orm import Session
from app.repositories.farmer_repo import FarmerRepository
from app.repositories.parcel_repo import ParcelRepository
from app.repositories.report_repo import ReportRepository
from app.repositories.index_repo import IndexRepository
from app.services.index_service import IndexInterpretationService
from datetime import datetime
from typing import List, Dict

class ReportGenerationService:
    def __init__(self, db: Session):
        self.farmer_repo = FarmerRepository(db)
        self.parcel_repo = ParcelRepository(db)
        self.report_repo = ReportRepository(db)
        self.index_repo = IndexRepository(db)
        self.interpretation_service = IndexInterpretationService()
    
    def generate_reports(self) -> List[Dict[str, str]]:
        """Generate reports for all farmers who should receive one today."""
        reports = []
        
        # Get all farmers with phone numbers (linked farmers)
        all_farmers = self.farmer_repo.get_all()
        linked_farmers = [f for f in all_farmers if f.phone]
        
        for farmer in linked_farmers:
            # Check if farmer should receive report today
            if self._should_receive_report_today(farmer.phone):
                message = self._generate_farmer_report(farmer)
                reports.append({
                    "to": farmer.phone,
                    "message": message
                })
        
        return reports
    
    def _should_receive_report_today(self, phone: str) -> bool:
        """Determine if a farmer should receive a report today based on their frequency."""
        farmer_report = self.report_repo.get_by_phone(phone)
        
        if not farmer_report:
            # No preference set, use default weekly
            # For this demo, we'll say weekly reports go out (simplified logic)
            return False
        
        frequency = farmer_report.report_frequency.lower()
        
        if frequency == "none":
            return False
        elif frequency == "daily":
            return True
        elif frequency == "weekly":
            # Simplified: assume weekly reports go out (in real system, check last sent date)
            return True
        elif "days" in frequency:
            # Simplified: for custom days, we'll send report (in real system, track last sent date)
            return True
        
        return False
    
    def _generate_farmer_report(self, farmer) -> str:
        """Generate a comprehensive report for a farmer about all their parcels."""
        parcels = self.parcel_repo.get_by_farmer_id(farmer.id)
        
        if not parcels:
            return f"Your weekly parcel report: You have no parcels registered."
        
        # Build report with simple summaries
        parcel_summaries = []
        
        for parcel in parcels:
            # Get latest indices for this parcel
            indices = self.index_repo.get_by_parcel_id(parcel.id)
            
            if not indices:
                parcel_summaries.append(f"Parcel {parcel.id} is stable")
                continue
            
            # Get the most recent index
            latest_index = indices[-1]
            
            # Get simple status interpretations
            veg_status = self.interpretation_service.vegetation_status(latest_index.ndvi)
            moisture_status = self.interpretation_service.moisture_status(latest_index.ndmi)
            nitrogen_status = self.interpretation_service.soil_nitrogen_status(latest_index.nitrogen)
            ph_status = self.interpretation_service.soil_ph_status(latest_index.ph)
            
            # Build concise status parts
            status_parts = []
            if veg_status:
                status_parts.append(veg_status)
            if moisture_status:
                status_parts.append(moisture_status)
            if nitrogen_status:
                status_parts.append(nitrogen_status)
            if ph_status:
                status_parts.append(ph_status)
            
            if status_parts:
                summary = f"Parcel {parcel.id} is stable, {', '.join(status_parts)}"
            else:
                summary = f"Parcel {parcel.id} is stable"
            
            parcel_summaries.append(summary)
        
        # Create final message
        return f"Your weekly parcel report: {'. '.join(parcel_summaries)}."
