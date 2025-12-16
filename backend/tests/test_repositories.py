import pytest
from app.repositories.farmer_repo import FarmerRepository
from app.repositories.parcel_repo import ParcelRepository
from app.repositories.index_repo import IndexRepository
from app.repositories.report_repo import ReportRepository
from app.models.base import Farmer, Parcel, ParcelIndex, FarmerReport
from datetime import date

class TestFarmerRepository:
    
    def test_get_by_phone(self, test_db, sample_farmer):
        """Test getting farmer by phone."""
        repo = FarmerRepository(test_db)
        farmer = repo.get_by_phone(sample_farmer.phone)
        
        assert farmer is not None
        assert farmer.id == sample_farmer.id
    
    def test_get_by_username(self, test_db, sample_farmer):
        """Test getting farmer by username."""
        repo = FarmerRepository(test_db)
        farmer = repo.get_by_username(sample_farmer.username)
        
        assert farmer is not None
        assert farmer.id == sample_farmer.id
    
    def test_get_all(self, test_db, sample_farmer):
        """Test getting all farmers."""
        repo = FarmerRepository(test_db)
        farmers = repo.get_all()
        
        assert len(farmers) >= 1
        assert any(f.id == sample_farmer.id for f in farmers)

class TestParcelRepository:
    
    def test_get_by_farmer_id(self, test_db, sample_farmer, sample_parcel):
        """Test getting parcels by farmer ID."""
        repo = ParcelRepository(test_db)
        parcels = repo.get_by_farmer_id(sample_farmer.id)
        
        assert len(parcels) >= 1
        assert parcels[0].id == sample_parcel.id
    
    def test_get_by_id(self, test_db, sample_parcel):
        """Test getting parcel by ID."""
        repo = ParcelRepository(test_db)
        parcel = repo.get_by_id(sample_parcel.id)
        
        assert parcel is not None
        assert parcel.name == sample_parcel.name
    
    def test_get_all(self, test_db, sample_parcel):
        """Test getting all parcels."""
        repo = ParcelRepository(test_db)
        parcels = repo.get_all()
        
        assert len(parcels) >= 1

class TestIndexRepository:
    
    def test_get_by_parcel_id(self, test_db, sample_parcel, sample_indices):
        """Test getting indices by parcel ID."""
        repo = IndexRepository(test_db)
        indices = repo.get_by_parcel_id(sample_parcel.id)
        
        assert len(indices) == 2
        assert all(idx.parcel_id == sample_parcel.id for idx in indices)

class TestReportRepository:
    
    def test_get_by_phone(self, test_db, sample_report):
        """Test getting report by phone."""
        repo = ReportRepository(test_db)
        report = repo.get_by_phone(sample_report.phone)
        
        assert report is not None
        assert report.id == sample_report.id
    
    def test_create_or_update_new(self, test_db):
        """Test creating new report."""
        repo = ReportRepository(test_db)
        report = repo.create_or_update("+40745555555", "daily")
        
        assert report is not None
        assert report.report_frequency == "daily"
    
    def test_update_last_sent(self, test_db, sample_report):
        """Test updating last_sent date."""
        repo = ReportRepository(test_db)
        test_date = date(2024, 1, 15)
        
        repo.update_last_sent(sample_report.phone, test_date)
        
        test_db.refresh(sample_report)
        assert sample_report.last_sent == test_date
