import pytest
from datetime import date, timedelta
from app.services.report_generation_service import ReportGenerationService
from app.models.base import FarmerReport

class TestReportGenerationService:
    
    def test_should_receive_report_daily(self, test_db, sample_farmer):
        """Test daily report frequency."""
        report = FarmerReport(
            id="REP002",
            phone=sample_farmer.phone,
            report_frequency="daily",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportGenerationService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    def test_should_receive_report_weekly_never_sent(self, test_db, sample_farmer):
        """Test weekly report when never sent before."""
        report = FarmerReport(
            id="REP003",
            phone=sample_farmer.phone,
            report_frequency="weekly",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportGenerationService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    
    def test_should_receive_report_custom_days(self, test_db, sample_farmer):
        """Test custom days report frequency."""
        report = FarmerReport(
            id="REP006",
            phone=sample_farmer.phone,
            report_frequency="3 days",
            last_sent=date.today() - timedelta(days=3)
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportGenerationService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is True
    
    def test_should_not_receive_report_none(self, test_db, sample_farmer):
        """Test 'none' frequency."""
        report = FarmerReport(
            id="REP007",
            phone=sample_farmer.phone,
            report_frequency="none",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportGenerationService(test_db)
        should_receive = service._should_receive_report_today(sample_farmer.phone)
        
        assert should_receive is False
    
    def test_generate_farmer_report_with_data(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test generating report for farmer with parcel data."""
        service = ReportGenerationService(test_db)
        report = service._generate_farmer_report(sample_farmer)
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert sample_parcel.id in report
    
    
    def test_generate_reports_updates_last_sent(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test that generate_reports updates last_sent date."""
        report = FarmerReport(
            id="REP008",
            phone=sample_farmer.phone,
            report_frequency="daily",
            last_sent=None
        )
        test_db.add(report)
        test_db.commit()
        
        service = ReportGenerationService(test_db)
        reports = service.generate_reports()
        
        # Verify last_sent was updated
        test_db.refresh(report)
        assert report.last_sent == date.today()
