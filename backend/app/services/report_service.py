from sqlalchemy.orm import Session
from app.repositories.report_repo import ReportRepository
from app.repositories.farmer_repo import FarmerRepository
from app.repositories.parcel_repo import ParcelRepository
from app.repositories.index_repo import IndexRepository
from app.ai.factory import get_summary_generator
from datetime import datetime, timedelta, date
from typing import List, Dict

class ReportService:
    def __init__(self, db: Session):
        self.report_repo = ReportRepository(db)
        self.farmer_repo = FarmerRepository(db)
        self.parcel_repo = ParcelRepository(db)
        self.index_repo = IndexRepository(db)
        self.summary_generator = get_summary_generator()
    
    def set_report_frequency(self, phone: str, frequency: str) -> str:
        """Set report frequency for a farmer."""
        # Validate frequency format
        valid_frequencies = ["daily", "weekly"]
        is_custom_days = frequency.endswith(" days") and frequency.split()[0].isdigit()
        
        if frequency not in valid_frequencies and not is_custom_days:
            return "Invalid frequency. Please use 'daily', 'weekly', or specify a number of days (e.g., '2 days')."
        
        # Create or update preference
        self.report_repo.create_or_update(phone, frequency)
        
        return f"Your report frequency has been set to {frequency}. You will receive parcel summaries every {frequency}."
    
    def get_report_frequency(self, phone: str) -> str:
        """Get current report frequency for a farmer."""
        report = self.report_repo.get_by_phone(phone)
        
        if report:
            return report.report_frequency
        
        return "none"  # Default frequency

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
                # Update last_sent date
                self.report_repo.update_last_sent(farmer.phone, date.today())
        
        return reports
    
    def _should_receive_report_today(self, phone: str) -> bool:
        """Determine if a farmer should receive a report today based on their frequency."""
        farmer_report = self.report_repo.get_by_phone(phone)
        
        if not farmer_report:
            # No preference set, don't send report
            return False
        
        frequency = farmer_report.report_frequency.lower()
        today = date.today()
        
        if frequency == "none":
            return False
        elif frequency == "daily":
            return True
        elif frequency == "weekly":
            # Check if 7 days have passed since last report
            if farmer_report.last_sent is None:
                return True  # Never sent before, send now
            days_since_last = (today - farmer_report.last_sent).days
            return days_since_last >= 7
        
        elif "days" in frequency:
            # Extract number of days from frequency like "2 days" or "3 days"
            try:
                days_interval = int(frequency.split()[0])
                if farmer_report.last_sent is None:
                    return True  # Never sent before, send now
                days_since_last = (today - farmer_report.last_sent).days
                return days_since_last >= days_interval
            except (ValueError, IndexError):
                return False
        
        return False
    
    def _generate_farmer_report(self, farmer) -> str:
        """Generate a comprehensive report for a farmer about all their parcels."""
        parcels = self.parcel_repo.get_by_farmer_id(farmer.id)
        
        if not parcels:
            return f"Your weekly parcel report: You have no parcels registered."
        
        # Build report with summaries (rule-based or LLM-powered)
        parcel_summaries = []
        
        for parcel in parcels:
            # Get latest indices for this parcel
            indices = self.index_repo.get_by_parcel_id(parcel.id)
            
            if not indices:
                parcel_summaries.append(f"Parcel {parcel.id}: no data available yet")
                continue
            
            # Sort indices by date to ensure we get the latest one
            indices.sort(key=lambda x: x.date)
            
            # Get the most recent index
            latest_index = indices[-1]
            
            # Use factory-generated summary generator (rule-based or LLM)
            indices_data = {
                "latest_index": latest_index,
                "parcel_name": parcel.name,
                "area_ha": parcel.area_ha,
                "crop": parcel.crop
            }
            summary = self.summary_generator.generate_parcel_summary(parcel.id, indices_data)
            
            parcel_summaries.append(summary)
        
        # Create final message
        return f"Your weekly parcel report: {'. '.join(parcel_summaries)}."
