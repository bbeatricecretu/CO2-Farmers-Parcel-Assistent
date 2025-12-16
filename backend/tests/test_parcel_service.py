import pytest
from app.services.parcel_service import ParcelService

class TestParcelService:
    
    def test_get_all_parcels(self, test_db, sample_parcel):
        """Test getting all parcels."""
        service = ParcelService(test_db)
        parcels = service.get_all_parcels()
        
        assert len(parcels) >= 1
        assert any(p.id == sample_parcel.id for p in parcels)
    
    def test_get_farmer_parcels(self, test_db, sample_farmer, sample_parcel):
        """Test getting parcels by farmer ID."""
        service = ParcelService(test_db)
        parcels = service.get_farmer_parcels(sample_farmer.id)
        
        assert len(parcels) >= 1
        assert all(p.farmer_id == sample_farmer.id for p in parcels)
    
    def test_format_parcels_list(self, test_db, sample_farmer, sample_parcel):
        """Test formatting parcels list."""
        service = ParcelService(test_db)
        formatted = service.format_parcels_list(sample_farmer)
        
        assert sample_parcel.id in formatted
        assert sample_parcel.crop in formatted
        assert "ha" in formatted.lower()
    
    def test_get_parcel_details(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test getting parcel details."""
        service = ParcelService(test_db)
        details = service.get_parcel_details(sample_parcel.id, sample_farmer)
        
        assert sample_parcel.name in details
        assert sample_parcel.crop in details
        assert str(sample_parcel.area_ha) in details
    
    def test_get_parcel_status(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test getting parcel status."""
        service = ParcelService(test_db)
        status = service.get_parcel_status(sample_parcel.id, sample_farmer)
        
        assert isinstance(status, str)
        assert len(status) > 0
