"""Trend summary generation strategies."""
from typing import Protocol, Dict
from app.ai.prompts import get_trend_analysis_summary_prompt

class TrendSummarizer(Protocol):
    """Protocol for trend summary generation strategies."""
    
    def generate_trend_summary(self, parcel_id: str, parcel_name: str, trends_data: Dict) -> str:
        """Generate a summary of the trend analysis."""
        ...

class RuleBasedTrendSummarizer:
    """Generate trend summaries using rule-based templates."""
    
    def generate_trend_summary(self, parcel_id: str, parcel_name: str, trends_data: Dict) -> str:
        """Generate a simple rule-based summary."""
        summary_parts = []
        
        trends = trends_data.get("trends", {})
        
        for index_name, data in trends.items():
            if isinstance(data, dict) and "trend" in data:
                trend = data["trend"]
                # Capitalize index name
                name = index_name.upper()
                summary_parts.append(f"{name}: {trend}")
        
        if not summary_parts:
            return "No trend data available."
            
        return f"Trend Analysis for {parcel_name}: " + ", ".join(summary_parts)

class LLMTrendSummarizer:
    """Generate trend summaries using an LLM."""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def generate_trend_summary(self, parcel_id: str, parcel_name: str, trends_data: Dict) -> str:
        """Generate an LLM-powered trend summary."""
        trends = trends_data.get("trends", {})
        
        prompt = get_trend_analysis_summary_prompt(parcel_id, parcel_name, trends)
        
        try:
            summary = self.llm_client.generate(prompt)
            return summary.strip()
        except Exception as e:
            print(f"LLM trend summary generation failed: {e}. Falling back to rule-based.")
            rule_based = RuleBasedTrendSummarizer()
            return rule_based.generate_trend_summary(parcel_id, parcel_name, trends_data)
