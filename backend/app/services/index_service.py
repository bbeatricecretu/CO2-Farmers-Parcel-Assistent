class IndexInterpretationService:
    """Service for interpreting parcel index values with rule-based logic."""
    
    @staticmethod
    def vegetation_status(value: float | None) -> str | None:
        """Interpret NDVI (Normalized Difference Vegetation Index)."""
        if value is None:
            return None
        if value < 0.30:
            return "vegetation is poor"
        elif value < 0.55:
            return "vegetation is moderate"
        elif value <= 0.75:
            return "vegetation is healthy"
        else:
            return "vegetation is very vigorous"
    
    @staticmethod
    def ndvi_status(value: float) -> str:
        """Interpret NDVI (Normalized Difference Vegetation Index)."""
        if value is None:
            return "No data available"
        if value < 0.30:
            return "Vegetation is poor and may be stressed."
        elif value < 0.55:
            return "Vegetation is developing with moderate health."
        elif value <= 0.75:
            return "Vegetation is healthy and dense."
        else:
            return "Vegetation is extremely vigorous."
    
    @staticmethod
    def moisture_status(value: float | None) -> str | None:
        """Interpret NDMI (Moisture Index)."""
        if value is None:
            return None
        if value < 0.15:
            return "moisture is low"
        elif value <= 0.30:
            return "moisture is moderate"
        else:
            return "moisture is high"
    
    @staticmethod
    def ndmi_status(value: float) -> str:
        """Interpret NDMI (Moisture Index)."""
        if value is None:
            return "No data available"
        if value < 0.15:
            return "Low moisture - possible drought stress."
        elif value <= 0.30:
            return "Moderate moisture levels."
        else:
            return "High moisture - healthy water content."
    
    @staticmethod
    def ndwi_status(value: float) -> str:
        """Interpret NDWI (Water Index)."""
        if value is None:
            return "No data available"
        if value < 0.10:
            return "Low water presence."
        elif value <= 0.25:
            return "Moderate water content."
        else:
            return "Strong water presence."
    
    @staticmethod
    def soc_status(value: float) -> str:
        """Interpret SOC (Soil Organic Carbon)."""
        if value is None:
            return "No data available"
        if value < 1.5:
            return "Low soil organic matter - poor soil quality."
        elif value <= 2.5:
            return "Moderate soil organic content."
        else:
            return "High organic content - rich soil quality."
    
    @staticmethod
    def soil_nitrogen_status(value: float | None) -> str | None:
        """Interpret Nitrogen levels."""
        if value is None:
            return None
        if value < 0.7:
            return "nitrogen is low"
        elif value <= 1.0:
            return "nitrogen is adequate"
        else:
            return "nitrogen is high"
    
    @staticmethod
    def nitrogen_status(value: float) -> str:
        """Interpret Nitrogen levels."""
        if value is None:
            return "No data available"
        if value < 0.7:
            return "Low nitrogen - crop may need fertilization."
        elif value <= 1.0:
            return "Adequate nitrogen levels."
        else:
            return "High nitrogen levels - good for crop growth."
    
    @staticmethod
    def phosphorus_status(value: float) -> str:
        """Interpret Phosphorus levels."""
        if value is None:
            return "No data available"
        if value < 0.35:
            return "Low phosphorus levels."
        elif value <= 0.45:
            return "Adequate phosphorus levels."
        else:
            return "High phosphorus levels."
    
    @staticmethod
    def soil_ph_status(value: float | None) -> str | None:
        """Interpret pH levels."""
        if value is None:
            return None
        if value < 5.5:
            return "pH is acidic"
        elif value <= 7.5:
            return "pH is neutral"
        else:
            return "pH is alkaline"
    
    @staticmethod
    def potassium_status(value: float) -> str:
        """Interpret Potassium levels."""
        if value is None:
            return "No data available"
        if value < 0.55:
            return "Low potassium levels."
        elif value <= 0.7:
            return "Adequate potassium levels."
        else:
            return "High potassium levels - good for crop health."
    
    @staticmethod
    def ph_status(value: float) -> str:
        """Interpret pH levels."""
        if value is None:
            return "No data available"
        if value < 5.5:
            return "Acidic soil - problematic for most crops."
        elif value < 6.0:
            return "Slightly acidic - acceptable for most crops."
        elif value <= 7.0:
            return "Good pH - ideal for most crops."
        else:
            return "Alkaline soil - may cause nutrient availability issues."
