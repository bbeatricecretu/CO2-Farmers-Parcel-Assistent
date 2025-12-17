"""Summary generation strategies for parcel reports."""
from app.services.index_service import IndexInterpretationService
from app.ai.prompts import get_parcel_summary_prompt

class RuleBasedSummaryGenerator:
    """Generate summaries using rule-based interpretation."""
    
    def __init__(self):
        self.interpretation_service = IndexInterpretationService()
    
    def generate_parcel_summary(self, parcel_id: str, indices_data: dict) -> str:
        """Generate a rule-based summary."""
        latest = indices_data.get("latest_index")
        parcel_name = indices_data.get("parcel_name", parcel_id)
        area = indices_data.get("area_ha", "?")
        crop = indices_data.get("crop", "Unknown")
        
        if not latest:
            return f"Parcel {parcel_id}: no data available yet"
            
        # Generate status summary
        summary = f"**Status Summary for Parcel {parcel_id}: {parcel_name}**\n"
        summary += f"({area} ha, {crop})\n"
        summary += f"Data from: {latest.date}\n\n"
        
        # Vegetation status
        if latest.ndvi is not None:
            summary += f"🌱 **Vegetation (NDVI: {latest.ndvi:.2f}):** {self.interpretation_service.ndvi_status(latest.ndvi)}\n\n"
        
        # Moisture status
        if latest.ndmi is not None:
            summary += f"💧 **Moisture (NDMI: {latest.ndmi:.2f}):** {self.interpretation_service.ndmi_status(latest.ndmi)}\n\n"
        
        # Water status
        if latest.ndwi is not None:
            summary += f"💦 **Water (NDWI: {latest.ndwi:.2f}):** {self.interpretation_service.ndwi_status(latest.ndwi)}\n\n"
        
        # Soil organic carbon
        if latest.soc is not None:
            summary += f"🌾 **Soil Organic Carbon (SOC: {latest.soc:.2f}):** {self.interpretation_service.soc_status(latest.soc)}\n\n"
        
        # Nitrogen
        if latest.nitrogen is not None:
            summary += f"🧪 **Nitrogen (N: {latest.nitrogen:.2f}):** {self.interpretation_service.nitrogen_status(latest.nitrogen)}\n\n"
        
        # Phosphorus
        if latest.phosphorus is not None:
            summary += f"🧪 **Phosphorus (P: {latest.phosphorus:.2f}):** {self.interpretation_service.phosphorus_status(latest.phosphorus)}\n\n"
        
        # Potassium
        if latest.potassium is not None:
            summary += f"🧪 **Potassium (K: {latest.potassium:.2f}):** {self.interpretation_service.potassium_status(latest.potassium)}\n\n"
        
        # pH
        if latest.ph is not None:
            summary += f"⚗️ **pH Level ({latest.ph:.2f}):** {self.interpretation_service.ph_status(latest.ph)}\n"
        
        return summary


class LLMSummaryGenerator:
    """Generate natural language summaries using an LLM."""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.interpretation_service = IndexInterpretationService()
    
    def generate_parcel_summary(self, parcel_id: str, indices_data: dict) -> str:
        """Generate an LLM-powered summary using prompt engineering."""
        latest_index = indices_data.get("latest_index")
        parcel_name = indices_data.get("parcel_name", parcel_id)
        
        if not latest_index:
            return f"Parcel {parcel_id}: no data available yet"
        
        # Gather indices
        indices = {
            "ndvi": latest_index.ndvi,
            "ndmi": latest_index.ndmi,
            "ndwi": latest_index.ndwi,
            "nitrogen": latest_index.nitrogen,
            "phosphorus": latest_index.phosphorus,
            "potassium": latest_index.potassium,
            "ph": latest_index.ph,
            "soc": latest_index.soc
        }
        
        # Get rule-based interpretations to provide context to LLM
        interpretations = {
            "vegetation": self.interpretation_service.vegetation_status(latest_index.ndvi),
            "moisture": self.interpretation_service.moisture_status(latest_index.ndmi),
            "nitrogen": self.interpretation_service.soil_nitrogen_status(latest_index.nitrogen),
            "ph": self.interpretation_service.soil_ph_status(latest_index.ph),
            "date": str(latest_index.date)
        }
        
        # Use engineered prompt
        prompt = get_parcel_summary_prompt(parcel_id, parcel_name, indices, interpretations)
        
        try:
            summary = self.llm_client.generate(prompt)
            return summary.strip()
        except Exception as e:
            # Fallback to rule-based if LLM fails
            print(f"LLM generation failed: {e}. Falling back to rule-based.")
            rule_based = RuleBasedSummaryGenerator()
            return rule_based.generate_parcel_summary(parcel_id, indices_data)
