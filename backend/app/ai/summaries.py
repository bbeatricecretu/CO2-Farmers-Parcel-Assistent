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
        
        # Counters for overall status
        good_count = 0
        moderate_count = 0
        poor_count = 0
        total_indices = 0
        
        # Generate status summary
        summary = f"**Current Status for Parcel {parcel_id} - {parcel_name}**\n"
        summary += f"({area} ha, {crop})\n\n"
        
        # Vegetation status (NDVI)
        if latest.ndvi is not None:
            total_indices += 1
            status_text = self.interpretation_service.ndvi_status(latest.ndvi)
            if latest.ndvi >= 0.55:
                good_count += 1
            elif latest.ndvi >= 0.30:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Vegetation (NDVI: {latest.ndvi:.2f}):** {status_text}\n\n"
        
        # Moisture status (NDMI)
        if latest.ndmi is not None:
            total_indices += 1
            status_text = self.interpretation_service.ndmi_status(latest.ndmi)
            if latest.ndmi > 0.30:
                good_count += 1
            elif latest.ndmi >= 0.15:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Moisture (NDMI: {latest.ndmi:.2f}):** {status_text}\n\n"
        
        # Water status (NDWI)
        if latest.ndwi is not None:
            total_indices += 1
            status_text = self.interpretation_service.ndwi_status(latest.ndwi)
            if latest.ndwi > 0.25:
                good_count += 1
            elif latest.ndwi >= 0.10:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Water (NDWI: {latest.ndwi:.2f}):** {status_text}\n\n"
        
        # Soil organic carbon (SOC)
        if latest.soc is not None:
            total_indices += 1
            status_text = self.interpretation_service.soc_status(latest.soc)
            if latest.soc > 2.5:
                good_count += 1
            elif latest.soc >= 1.5:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Soil Organic Carbon (SOC: {latest.soc:.2f}):** {status_text}\n\n"
        
        # Nitrogen
        if latest.nitrogen is not None:
            total_indices += 1
            status_text = self.interpretation_service.nitrogen_status(latest.nitrogen)
            if latest.nitrogen > 1.0:
                good_count += 1
            elif latest.nitrogen >= 0.7:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Nitrogen (N: {latest.nitrogen:.2f}):** {status_text}\n\n"
        
        # Phosphorus
        if latest.phosphorus is not None:
            total_indices += 1
            status_text = self.interpretation_service.phosphorus_status(latest.phosphorus)
            if latest.phosphorus > 0.45:
                good_count += 1
            elif latest.phosphorus >= 0.35:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Phosphorus (P: {latest.phosphorus:.2f}):** {status_text}\n\n"
        
        # Potassium
        if latest.potassium is not None:
            total_indices += 1
            status_text = self.interpretation_service.potassium_status(latest.potassium)
            if latest.potassium > 0.7:
                good_count += 1
            elif latest.potassium >= 0.55:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**Potassium (K: {latest.potassium:.2f}):** {status_text}\n\n"
        
        # pH
        if latest.ph is not None:
            total_indices += 1
            status_text = self.interpretation_service.ph_status(latest.ph)
            if 6.0 <= latest.ph <= 7.0:
                good_count += 1
            elif 5.5 <= latest.ph < 6.0 or 7.0 < latest.ph <= 7.5:
                moderate_count += 1
            else:
                poor_count += 1
            summary += f"**pH Level ({latest.ph:.2f}):** {status_text}\n\n"
        
        # Calculate overall status
        if total_indices > 0:
            summary += "---\n\n"
            summary += f"**Overall Parcel Status:**\n"
            summary += f"- Good: {good_count}/{total_indices} indices\n"
            summary += f"- Moderate: {moderate_count}/{total_indices} indices\n"
            summary += f"- Poor: {poor_count}/{total_indices} indices\n\n"
            
            # Determine overall status based on majority
            if good_count >= total_indices * 0.6:
                overall = " **EXCELLENT** - Parcel is in great condition"
                recommendation = "Continue current management practices. This parcel is performing optimally. Monitor regularly to maintain these excellent conditions."
            elif good_count + moderate_count >= total_indices * 0.7:
                overall = " **GOOD** - Parcel is performing well with minor areas for improvement"
                recommendation = "The parcel is in good health. Focus on improving the moderate indices through targeted interventions such as adjusting irrigation or applying specific fertilizers where needed."
            elif poor_count >= total_indices * 0.5:
                overall = " **NEEDS ATTENTION** - Multiple indices require immediate action"
                recommendation = "Immediate action required. Review poor indices and implement corrective measures: consider soil amendments, adjust irrigation schedules, apply necessary fertilizers, and consult an agronomist if conditions persist."
            else:
                overall = " **MODERATE** - Parcel needs monitoring and possible interventions"
                recommendation = "Regular monitoring is advised. Address declining indices before they become critical. Consider preventive measures such as balanced fertilization and proper water management."
            
            summary += f"**Summary: {overall}. **\n\n"
            summary += f"{recommendation}. \n\n"
            
        summary += f"Last measured on {latest.date}.\n\n"
        
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
