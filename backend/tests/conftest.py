import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base, Farmer, Parcel, ParcelIndex, FarmerReport
from datetime import date, datetime

#Integration test
# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_farmer(test_db):
    """Create a sample farmer for testing."""
    farmer = Farmer(
        id="F001",
        username="john_doe",
        name="John Doe",
        phone="+40741111111"
    )
    test_db.add(farmer)
    test_db.commit()
    test_db.refresh(farmer)
    return farmer

@pytest.fixture
def sample_parcel(test_db, sample_farmer):
    """Create a sample parcel for testing."""
    parcel = Parcel(
        id="P001",
        farmer_id=sample_farmer.id,
        name="Field 1",
        area_ha=10.5,
        crop="Wheat"
    )
    test_db.add(parcel)
    test_db.commit()
    test_db.refresh(parcel)
    return parcel

@pytest.fixture
def sample_indices(test_db, sample_parcel):
    """Create sample indices for testing."""
    indices = [
        ParcelIndex(
            id="IDX001",
            parcel_id=sample_parcel.id,
            date=date(2024, 1, 1),
            ndvi=0.7,
            ndmi=0.5,
            ndwi=0.3,
            nitrogen=50.0,
            ph=6.5
        ),
        ParcelIndex(
            id="IDX002",
            parcel_id=sample_parcel.id,
            date=date(2024, 2, 1),
            ndvi=0.8,
            ndmi=0.6,
            ndwi=0.4,
            nitrogen=55.0,
            ph=6.8
        )
    ]
    for index in indices:
        test_db.add(index)
    test_db.commit()
    return indices

@pytest.fixture
def sample_report(test_db, sample_farmer):
    """Create a sample farmer report for testing."""
    report = FarmerReport(
        id="REP001",
        phone=sample_farmer.phone,
        report_frequency="weekly",
        last_sent=None
    )
    test_db.add(report)
    test_db.commit()
    test_db.refresh(report)
    return report
