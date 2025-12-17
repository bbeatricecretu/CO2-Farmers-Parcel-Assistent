import pytest
from datetime import date, timedelta
from app.services.report_service import ReportService
from app.models.base import FarmerReport

class TestReportService:
    
    def test_should_receive_report_daily(self, test_db, sample_farmer):
        """Test daily report frequency."""
        report = FarmerReport(
            id="R1",
            phone=sample_farmer.phone,
            report_frequency="daily",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    def test_should_receive_report_weekly_never_sent(self, test_db, sample_farmer):
        """Test weekly report when never sent before."""
        report = FarmerReport(
            id="R2",
            phone=sample_farmer.phone,
            report_frequency="weekly",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    
    def test_should_receive_report_custom_days(self, test_db, sample_farmer):
        """Test custom days report frequency."""
        report = FarmerReport(
            id="R3",
            phone=sample_farmer.phone,
            report_frequency="3 days",
            last_sent=date.today() - timedelta(days=3)
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    def test_should_not_receive_report_none(self, test_db, sample_farmer):
        """Test 'none' frequency."""
        report = FarmerReport(
            id="R4",
            phone=sample_farmer.phone,
            report_frequency="none",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is False
    
    def test_generate_farmer_report_with_data(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test generating report for farmer with parcel data."""
        service = ReportService(test_db)
        report = service._generate_farmer_report(sample_farmer)
        
        assert isinstance(report, dict)
        assert "to" in report
        assert "farmer" in report
        assert "parcels" in report
        assert len(report["parcels"]) > 0
        assert report["parcels"][0]["parcel_id"] == sample_parcel.id
    
    
    def test_generate_reports_updates_last_sent(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test that generate_reports updates last_sent date."""
        report = FarmerReport(
            id="R5",
            phone=sample_farmer.phone,
            report_frequency="daily",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportService(test_db)
        reports = service.generate_reports()
        
        # Verify last_sent was updated
        test_db.refresh(report)
        assert report.last_sent == date.today()
