from sqlalchemy.orm import Session
from app.repositories.report_repo import ReportRepository

class ReportService:
    def __init__(self, db: Session):
        self.report_repo = ReportRepository(db)
    
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
