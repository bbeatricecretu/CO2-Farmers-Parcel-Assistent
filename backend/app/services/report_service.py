from sqlalchemy.orm import Session
from app.repositories.report_repo import ReportRepository
from app.repositories.farmer_repo import FarmerRepository
from app.repositories.parcel_repo import ParcelRepository
from app.repositories.index_repo import IndexRepository
from app.ai.factory import get_summary_generator
from app.services.index_service import IndexInterpretationService
from datetime import date
from typing import List, Dict

class ReportService:
    def __init__(self, db: Session):
        self.report_repo = ReportRepository(db)
        self.farmer_repo = FarmerRepository(db)
        self.parcel_repo = ParcelRepository(db)
        self.index_repo = IndexRepository(db)
        self.summary_generator = get_summary_generator()
        self.interpretation_service = IndexInterpretationService()
    
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

    def generate_reports(self) -> List[Dict]:
        """Generate reports for all farmers who should receive one today."""
        reports = []
        
        # Get all farmers with phone numbers (linked farmers)
        all_farmers = self.farmer_repo.get_all()
        linked_farmers = [f for f in all_farmers if f.phone]
        
        for farmer in linked_farmers:
            # Check if farmer should receive report today
            if self._should_receive_report_today(farmer.phone):
                report = self._generate_farmer_report(farmer)
                reports.append(report)
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
    
    def _generate_farmer_report(self, farmer) -> Dict:
        """Generate a comprehensive report for a farmer about all their parcels."""
        parcels = self.parcel_repo.get_by_farmer_id(farmer.id)
        
        # Get report frequency to determine report type
        frequency = self.get_report_frequency(farmer.phone)
        
        report_data = {
            "to": farmer.phone,
            "farmer": farmer.name,
            "report_type": frequency,
            "generated_at": date.today().strftime('%Y-%m-%d'),
            "parcels": []
        }
        
        if not parcels:
            return report_data
        
        # Build report with summaries (rule-based or LLM-powered)
        for parcel in parcels:
            # Get latest indices for this parcel
            indices = self.index_repo.get_by_parcel_id(parcel.id)
            
            if not indices:
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
            
            # Build structured parcel data
            def safe_round(value, decimals=2):
                return round(float(value), decimals) if value is not None else 0.0
            
            parcel_data = {
                "parcel_id": parcel.id,
                "name": parcel.name,
                "area_ha": float(parcel.area_ha),
                "crop": parcel.crop,
                "data_date": str(latest_index.date),
                "indices": {
                    "ndvi": {
                        "value": safe_round(latest_index.ndvi),
                        "status": self.interpretation_service.vegetation_status(latest_index.ndvi) if latest_index.ndvi else "unknown"
                    },
                    "ndmi": {
                        "value": safe_round(latest_index.ndmi),
                        "status": self.interpretation_service.moisture_status(latest_index.ndmi) if latest_index.ndmi else "unknown"
                    },
                    "ndwi": {
                        "value": safe_round(latest_index.ndwi),
                        "status": "moderate_water"
                    },
                    "soc": {
                        "value": safe_round(latest_index.soc),
                        "status": "moderate"
                    },
                    "n": {
                        "value": safe_round(latest_index.nitrogen),
                        "status": self.interpretation_service.soil_nitrogen_status(latest_index.nitrogen) if latest_index.nitrogen else "unknown"
                    },
                    "p": {
                        "value": safe_round(latest_index.phosphorus),
                        "status": "moderate"
                    },
                    "k": {
                        "value": safe_round(latest_index.potassium),
                        "status": "moderate"
                    },
                    "ph": {
                        "value": safe_round(latest_index.ph),
                        "status": self.interpretation_service.soil_ph_status(latest_index.ph) if latest_index.ph else "unknown"
                    }
                },
                "summary": summary
            }
            
            report_data["parcels"].append(parcel_data)
        
        return report_data
