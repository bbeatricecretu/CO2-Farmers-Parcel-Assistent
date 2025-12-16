import pytest
from app.services.index_service import IndexInterpretationService

class TestIndexInterpretationService:
    
    def setup_method(self):
        """Setup test instance."""
        self.service = IndexInterpretationService()
    
    # NDVI Tests
    def test_vegetation_status_healthy(self):
        """Test healthy vegetation status."""
        status = self.service.vegetation_status(0.7)
        assert "healthy" in status.lower()
    
    
    # NDMI Tests
    
    def test_moisture_status_low(self):
        """Test low moisture status."""
        status = self.service.moisture_status(0.1)
        assert "low" in status.lower()
    
    # Nitrogen Tests
    def test_nitrogen_status_good(self):
        """Test good nitrogen status."""
        status = self.service.soil_nitrogen_status(1.5)
        assert "high" in status.lower()
    
    def test_nitrogen_status_low(self):
        """Test low nitrogen status."""
        status = self.service.soil_nitrogen_status(0.5)
        assert "low" in status.lower()
    

    # pH Tests
    def test_ph_status_optimal(self):
        """Test optimal pH status."""
        status = self.service.soil_ph_status(6.5)
        assert "neutral" in status.lower()
    
    def test_ph_status_acidic(self):
        """Test acidic pH status."""
        status = self.service.soil_ph_status(5.0)
        assert "acidic" in status.lower() or "low" in status.lower()
    
    