import pytest
from app.services.farmer_service import FarmerService
from app.models.base import Farmer

class TestFarmerService:
    
    def test_get_by_phone_existing(self, test_db, sample_farmer):
        """Test getting farmer by existing phone number."""
        service = FarmerService(test_db)
        farmer = service.get_by_phone(sample_farmer.phone)
        
        assert farmer is not None
        assert farmer.phone == sample_farmer.phone
        assert farmer.username == sample_farmer.username
    
    def test_get_by_phone_non_existing(self, test_db):
        """Test getting farmer by non-existing phone number."""
        service = FarmerService(test_db)
        farmer = service.get_by_phone("+40799999999")
        
        assert farmer is None
    
    def test_get_by_username_existing(self, test_db, sample_farmer):
        """Test getting farmer by existing username."""
        service = FarmerService(test_db)
        farmer = service.get_by_username(sample_farmer.username)
        
        assert farmer is not None
        assert farmer.username == sample_farmer.username
        assert farmer.name == sample_farmer.name
    
    def test_get_by_username_non_existing(self, test_db):
        """Test getting farmer by non-existing username."""
        service = FarmerService(test_db)
        farmer = service.get_by_username("non_existing_user")
        
        assert farmer is None
    
    def test_link_account_success(self, test_db):
        """Test successfully linking account."""
        # Create a farmer without phone
        farmer = Farmer(
            id="F002",
            username="jane_smith",
            name="Jane Smith",
            phone=None
        )
        test_db.add(farmer)
        test_db.commit()
        
        service = FarmerService(test_db)
        result = service.link_account("+40742222222", "jane_smith")
        
        assert "linked" in result.lower()
        
        # Verify phone was added
        updated_farmer = service.get_by_username("jane_smith")
        assert updated_farmer.phone == "+40742222222"
    
    def test_link_account_invalid_username(self, test_db):
        """Test linking account with invalid username."""
        service = FarmerService(test_db)
        result = service.link_account("+40742222222", "invalid_user")
        
        assert "not found" in result.lower() or "error" in result.lower()
    
    def test_link_account_already_linked(self, test_db, sample_farmer):
        """Test linking account that is already linked."""
        service = FarmerService(test_db)
        result = service.link_account(sample_farmer.phone, sample_farmer.username)
        
        assert "already" in result.lower()
