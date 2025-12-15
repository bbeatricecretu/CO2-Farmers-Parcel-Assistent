from sqlalchemy.orm import Session
from app.models.database import FarmerPreference

class ReportRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_phone(self, phone: str):
        """Get farmer preference by phone number."""
        return self.db.query(FarmerPreference).filter(FarmerPreference.phone == phone).first()
    
    def create_or_update(self, phone: str, report_frequency: str):
        """Create or update farmer preference."""
        preference = self.get_by_phone(phone)
        
        if preference:
            preference.report_frequency = report_frequency
        else:
            import uuid
            preference = FarmerPreference(
                id=f"PREF_{uuid.uuid4().hex[:8].upper()}",
                phone=phone,
                report_frequency=report_frequency
            )
            self.db.add(preference)
        
        self.db.commit()
        self.db.refresh(preference)
        return preference
