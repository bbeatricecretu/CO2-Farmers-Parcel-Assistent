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
    """Create a sample farmer for testing - based on Ana Popescu from real data."""
    farmer = Farmer(
        id="F1",
        username="ana.popescu",
        name="Ana Popescu",
        phone="+40741111111"
    )
    test_db.add(farmer)
    test_db.commit()
    test_db.refresh(farmer)
    return farmer

@pytest.fixture
def sample_parcel(test_db, sample_farmer):
    """Create a sample parcel for testing - based on North Field from real data."""
    parcel = Parcel(
        id="P1",
        farmer_id=sample_farmer.id,
        name="North Field",
        area_ha=12.3,
        crop="Wheat"
    )
    test_db.add(parcel)
    test_db.commit()
    test_db.refresh(parcel)
    return parcel

@pytest.fixture
def sample_indices(test_db, sample_parcel):
    """Create sample indices for testing - based on real data patterns."""
    indices = [
        ParcelIndex(
            id="P1_IDX1",
            parcel_id=sample_parcel.id,
            date=date(2025, 4, 1),
            ndvi=0.42,
            ndmi=0.2,
            ndwi=0.15,
            soc=1.7,
            nitrogen=0.8,
            phosphorus=0.35,
            potassium=0.6,
            ph=6.4
        ),
        ParcelIndex(
            id="P1_IDX2",
            parcel_id=sample_parcel.id,
            date=date(2025, 5, 1),
            ndvi=0.63,
            ndmi=0.32,
            ndwi=0.22,
            soc=1.7,
            nitrogen=0.75,
            phosphorus=0.33,
            potassium=0.59,
            ph=6.4
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
