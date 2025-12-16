import pytest
from app.services.trend_analysis_service import TrendAnalysisService
from app.models.base import Parcel, ParcelIndex
from datetime import date

class TestTrendAnalysisService:
    
    def test_increasing_trend(self, test_db, sample_farmer):
        """Test detecting increasing trend (e.g., improving vegetation)."""
        # Create parcel
        parcel = Parcel(
            id="P_TREND1",
            farmer_id=sample_farmer.id,
            name="Trend Field",
            area_ha=10.0,
            crop="Wheat"
        )
        test_db.add(parcel)
        test_db.commit()
        
        # Add indices with increasing NDVI
        indices = [
            ParcelIndex(
                id="IDX1",
                parcel_id=parcel.id,
                date=date(2025, 4, 1),
                ndvi=0.4,
                nitrogen=0.8,
                ph=6.5
            ),
            ParcelIndex(
                id="IDX2",
                parcel_id=parcel.id,
                date=date(2025, 5, 1),
                ndvi=0.7,  # Increased by 0.3 - should be "increasing"
                nitrogen=0.75,
                ph=6.5
            )
        ]
        for idx in indices:
            test_db.add(idx)
        test_db.commit()
        
        service = TrendAnalysisService(test_db)
        result = service.analyze_parcel_trends(parcel.id)
        
        assert "trends" in result
        assert "ndvi" in result["trends"]
        assert result["trends"]["ndvi"]["trend"] == "increasing"
        assert "improving" in result["trends"]["ndvi"]["interpretation"].lower()
        assert "recommendation" in result["trends"]["ndvi"]
        assert len(result["trends"]["ndvi"]["recommendation"]) > 0
    
    def test_decreasing_trend(self, test_db, sample_farmer):
        """Test detecting decreasing trend (e.g., nitrogen depletion)."""
        parcel = Parcel(
            id="P_TREND2",
            farmer_id=sample_farmer.id,
            name="Depleting Field",
            area_ha=10.0,
            crop="Corn"
        )
        test_db.add(parcel)
        test_db.commit()
        
        # Add indices with decreasing nitrogen
        indices = [
            ParcelIndex(
                id="IDX3",
                parcel_id=parcel.id,
                date=date(2025, 4, 1),
                nitrogen=1.0,
                ndvi=0.6
            ),
            ParcelIndex(
                id="IDX4",
                parcel_id=parcel.id,
                date=date(2025, 5, 1),
                nitrogen=0.6,  # Decreased by 0.4 - should be "decreasing"
                ndvi=0.6
            )
        ]
        for idx in indices:
            test_db.add(idx)
        test_db.commit()
        
        service = TrendAnalysisService(test_db)
        result = service.analyze_parcel_trends(parcel.id)
        
        assert result["trends"]["nitrogen"]["trend"] == "decreasing"
        assert "depletion" in result["trends"]["nitrogen"]["interpretation"].lower()
        assert "recommendation" in result["trends"]["nitrogen"]
        assert "nitrogen" in result["trends"]["nitrogen"]["recommendation"].lower()
        assert "declining" in result["trends"]["nitrogen"]["recommendation"].lower() or "dropping" in result["trends"]["nitrogen"]["recommendation"].lower()
    
    def test_stable_trend(self, test_db, sample_farmer):
        """Test detecting stable trend (small changes)."""
        parcel = Parcel(
            id="P_TREND3",
            farmer_id=sample_farmer.id,
            name="Stable Field",
            area_ha=10.0,
            crop="Wheat"
        )
        test_db.add(parcel)
        test_db.commit()
        
        # Add indices with minimal change
        indices = [
            ParcelIndex(
                id="IDX5",
                parcel_id=parcel.id,
                date=date(2025, 4, 1),
                ph=6.5,
                ndvi=0.6
            ),
            ParcelIndex(
                id="IDX6",
                parcel_id=parcel.id,
                date=date(2025, 5, 1),
                ph=6.52,  # Changed by only 0.02 - should be "stable"
                ndvi=0.6
            )
        ]
        for idx in indices:
            test_db.add(idx)
        test_db.commit()
        
        service = TrendAnalysisService(test_db)
        result = service.analyze_parcel_trends(parcel.id)
        
        assert result["trends"]["ph"]["trend"] == "stable"
        assert "stable" in result["trends"]["ph"]["interpretation"].lower()
    
    def test_insufficient_data(self, test_db, sample_farmer):
        """Test handling insufficient data."""
        parcel = Parcel(
            id="P_TREND4",
            farmer_id=sample_farmer.id,
            name="New Field",
            area_ha=10.0,
            crop="Wheat"
        )
        test_db.add(parcel)
        test_db.commit()
        
        service = TrendAnalysisService(test_db)
        result = service.analyze_parcel_trends(parcel.id)
        
        assert result["status"] == "insufficient_data"
        assert result["data_points"] == 0
    
    def test_period_information(self, test_db, sample_farmer, sample_parcel, sample_indices):
        """Test that period information is included in results."""
        service = TrendAnalysisService(test_db)
        result = service.analyze_parcel_trends(sample_parcel.id)
        
        assert "period" in result
        assert "start_date" in result["period"]
        assert "end_date" in result["period"]
        assert result["period"]["data_points"] == 2
