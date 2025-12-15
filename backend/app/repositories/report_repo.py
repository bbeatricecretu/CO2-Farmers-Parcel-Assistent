from sqlalchemy.orm import Session
from app.models.database import FarmerReport
import uuid

class ReportRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_phone(self, phone: str):
        """Get farmer report by phone number."""
        return self.db.query(FarmerReport).filter(FarmerReport.phone == phone).first()
    
    def create_or_update(self, phone: str, report_frequency: str):
        """Create or update a farmer report."""
        report = self.get_by_phone(phone)
        
        if report:
            report.report_frequency = report_frequency
        else:
            report = FarmerReport(
                id=f"REP_{uuid.uuid4().hex[:8].upper()}",
                phone=phone,
                report_frequency=report_frequency
            )
            self.db.add(report)
        
        self.db.commit()
        return report
