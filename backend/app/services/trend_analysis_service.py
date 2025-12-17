from sqlalchemy.orm import Session
from app.repositories.index_repo import IndexRepository
from app.repositories.parcel_repo import ParcelRepository
from app.ai.factory import get_trend_summarizer
from typing import Dict

class TrendAnalysisService:
    """Service for analyzing trends in parcel indices over time."""
    
    def __init__(self, db: Session):
        self.index_repo = IndexRepository(db)
        self.parcel_repo = ParcelRepository(db)
        self.summarizer = get_trend_summarizer()
    
    def analyze_parcel_trends(self, parcel_id: str) -> Dict:
        """
        Analyze trends for all indices of a parcel.
        Uses a standard threshold of 0.05 for all indices to provide accurate trend detection.
        
        Threshold: 0.05 (5% change)
        - Change > 0.05 → increasing trend
        - Change < -0.05 → decreasing trend
        - Change between -0.05 and 0.05 → stable
        
        Args:
            parcel_id: The parcel ID
            
        Returns:
            Dictionary with trend analysis for each index
        """
        indices = self.index_repo.get_by_parcel_id(parcel_id)
        
        if not indices or len(indices) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 data points for trend analysis",
                "data_points": len(indices) if indices else 0
            }
        
        # Get parcel name
        parcel = self.parcel_repo.get_by_id(parcel_id)
        parcel_name = parcel.name if parcel else parcel_id
        
        # Sort by date
        indices.sort(key=lambda x: x.date)
        
        first = indices[0]
        last = indices[-1]
        
        trends = {
            "period": {
                "start_date": str(first.date),
                "end_date": str(last.date),
                "data_points": len(indices)
            },
            "trends": {}
        }
        
        # Analyze each index with standard 0.05 threshold
        if first.ndvi is not None and last.ndvi is not None:
            analysis = self._analyze_trend(
                first.ndvi, last.ndvi, 0.05,
                "vegetation", "improving", "declining"
            )
            analysis["recommendation"] = self._get_recommendation("ndvi", analysis["trend"], last.ndvi)
            trends["trends"]["ndvi"] = analysis
        
        if first.ndmi is not None and last.ndmi is not None:
            analysis = self._analyze_trend(
                first.ndmi, last.ndmi, 0.05,
                "moisture", "increasing", "decreasing"
            )
            analysis["recommendation"] = self._get_recommendation("ndmi", analysis["trend"], last.ndmi)
            trends["trends"]["ndmi"] = analysis
        
        if first.ndwi is not None and last.ndwi is not None:
            analysis = self._analyze_trend(
                first.ndwi, last.ndwi, 0.05,
                "water content", "increasing", "decreasing"
            )
            analysis["recommendation"] = self._get_recommendation("ndwi", analysis["trend"], last.ndwi)
            trends["trends"]["ndwi"] = analysis
        
        if first.soc is not None and last.soc is not None:
            analysis = self._analyze_trend(
                first.soc, last.soc, 0.05,
                "soil organic carbon", "increasing", "decreasing"
            )
            analysis["recommendation"] = self._get_recommendation("soc", analysis["trend"], last.soc)
            trends["trends"]["soc"] = analysis
        
        if first.nitrogen is not None and last.nitrogen is not None:
            analysis = self._analyze_trend(
                first.nitrogen, last.nitrogen, 0.05,
                "nitrogen", "increasing", "decreasing - potential nutrient depletion"
            )
            analysis["recommendation"] = self._get_recommendation("nitrogen", analysis["trend"], last.nitrogen)
            trends["trends"]["nitrogen"] = analysis
        
        if first.phosphorus is not None and last.phosphorus is not None:
            analysis = self._analyze_trend(
                first.phosphorus, last.phosphorus, 0.05,
                "phosphorus", "increasing", "decreasing"
            )
            analysis["recommendation"] = self._get_recommendation("phosphorus", analysis["trend"], last.phosphorus)
            trends["trends"]["phosphorus"] = analysis
        
        if first.potassium is not None and last.potassium is not None:
            analysis = self._analyze_trend(
                first.potassium, last.potassium, 0.05,
                "potassium", "increasing", "decreasing"
            )
            analysis["recommendation"] = self._get_recommendation("potassium", analysis["trend"], last.potassium)
            trends["trends"]["potassium"] = analysis
        
        if first.ph is not None and last.ph is not None:
            analysis = self._analyze_trend(
                first.ph, last.ph, 0.05,
                "pH", "increasing (more alkaline)", "decreasing (more acidic)"
            )
            analysis["recommendation"] = self._get_recommendation("ph", analysis["trend"], last.ph)
            trends["trends"]["ph"] = analysis
        
        # Generate summary using the configured strategy (Rule-based or LLM)
        trends["summary"] = self.summarizer.generate_trend_summary(parcel_id, parcel_name, trends)
        
        return trends
    
    def _analyze_trend(
        self, 
        first_value: float, 
        last_value: float, 
        threshold: float,
        metric_name: str,
        increasing_msg: str,
        decreasing_msg: str
    ) -> Dict:
        """
        Analyze trend for a single metric.
        
        Formulas:
        - Increasing: last_value - first_value > threshold
        - Decreasing: last_value - first_value < -threshold
        - Stable: abs(last_value - first_value) <= threshold
        """
        difference = last_value - first_value
        
        if difference > threshold:
            trend = "increasing"
            interpretation = f"{metric_name} is {increasing_msg}"
        elif difference < -threshold:
            trend = "decreasing"
            interpretation = f"{metric_name} is {decreasing_msg}"
        else:
            trend = "stable"
            interpretation = f"{metric_name} is stable"
        
        return {
            "trend": trend,
            "first_value": round(first_value, 3),
            "last_value": round(last_value, 3),
            "change": round(difference, 3),
            "interpretation": interpretation
        }
    
    def _get_recommendation(self, index_name: str, trend: str, last_value: float) -> str:
        """Get explanation based on index trend and current value."""
        explanations = {
            "ndvi": {
                "increasing": "Vegetation density and health are improving, indicating stronger crop canopy development.",
                "decreasing": "Vegetation density is declining, which may indicate crop stress, disease, or reduced plant vigor.",
                "stable": "Vegetation density remains consistent with no significant changes in crop canopy health."
            },
            "ndmi": {
                "increasing": "Moisture content in vegetation is rising, suggesting better water availability in plant tissues.",
                "decreasing": "Moisture content is declining, indicating potential water stress or drought conditions developing.",
                "stable": "Moisture levels remain steady with consistent water content in the vegetation."
            },
            "ndwi": {
                "increasing": "Water presence is increasing, showing improved water availability in the soil and crops.",
                "decreasing": "Water content is reducing, which reflects drier conditions or reduced water retention.",
                "stable": "Water levels are maintaining equilibrium with no significant moisture fluctuations."
            },
            "soc": {
                "increasing": "Soil organic carbon is accumulating, reflecting improved soil structure and organic matter content.",
                "decreasing": "Organic carbon levels are declining, suggesting organic matter decomposition or soil degradation.",
                "stable": "Soil organic carbon remains constant, indicating balanced organic matter dynamics."
            },
            "nitrogen": {
                "increasing": "Nitrogen availability is growing, showing improved nutrient supply for plant growth.",
                "decreasing": "Nitrogen levels are dropping, indicating nutrient uptake by crops or nutrient loss from the soil.",
                "stable": "Nitrogen content remains balanced with consistent nutrient availability."
            },
            "phosphorus": {
                "increasing": "Phosphorus levels are rising, indicating increased availability of this essential nutrient.",
                "decreasing": "Phosphorus is declining, reflecting nutrient consumption or reduced availability in soil.",
                "stable": "Phosphorus levels remain steady with balanced nutrient dynamics."
            },
            "potassium": {
                "increasing": "Potassium content is growing, showing improved availability of this important macronutrient.",
                "decreasing": "Potassium levels are falling, indicating nutrient depletion or increased plant uptake.",
                "stable": "Potassium remains at consistent levels with stable nutrient status."
            },
            "ph": {
                "increasing": "Soil pH is rising, meaning the soil is becoming more alkaline or less acidic.",
                "decreasing": "Soil pH is falling, indicating the soil is becoming more acidic or less alkaline.",
                "stable": "Soil pH remains constant with no significant changes in acidity or alkalinity."
            }
        }
        
        return explanations.get(index_name, {}).get(trend, "This metric shows a trend pattern over the analyzed period.")
