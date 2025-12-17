"""Summary generation strategies for parcel reports."""
from typing import Protocol
from app.services.index_service import IndexInterpretationService
from app.ai.prompts import get_parcel_summary_prompt


class SummaryGenerator(Protocol):
    """Protocol for summary generation strategies."""
    
    # A Protocol defines a contract
    # Any summary generator must have a generate_parcel_summary(...) method.
    def generate_parcel_summary(self, parcel_id: str, indices_data: dict) -> str:
        """Generate a summary for a parcel based on its index data."""
        ...


class RuleBasedSummaryGenerator:
    """Generate summaries using rule-based interpretation."""
    
    def __init__(self):
        self.interpretation_service = IndexInterpretationService()
    
    def generate_parcel_summary(self, parcel_id: str, indices_data: dict) -> str:
        """Generate a rule-based summary."""
        latest_index = indices_data.get("latest_index")
        
        if not latest_index:
            return f"Parcel {parcel_id}: no data available yet"
        
        # Get simple status interpretations
        veg_status = self.interpretation_service.vegetation_status(latest_index.ndvi)
        moisture_status = self.interpretation_service.moisture_status(latest_index.ndmi)
        nitrogen_status = self.interpretation_service.soil_nitrogen_status(latest_index.nitrogen)
        ph_status = self.interpretation_service.soil_ph_status(latest_index.ph)
        
        # Build concise status parts
        status_parts = []
        if veg_status:
            status_parts.append(veg_status)
        if moisture_status:
            status_parts.append(moisture_status)
        if nitrogen_status:
            status_parts.append(nitrogen_status)
        if ph_status:
            status_parts.append(ph_status)
        
        if status_parts:
            summary = f"Parcel {parcel_id} is stable, {', '.join(status_parts)}"
        else:
            summary = f"Parcel {parcel_id} is stable"
        
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
            "ph": self.interpretation_service.soil_ph_status(latest_index.ph)
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
