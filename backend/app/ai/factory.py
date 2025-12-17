"""Factory for creating summary generators."""
import os
from app.ai.summaries import RuleBasedSummaryGenerator, LLMSummaryGenerator


# Decides which implementation to use at runtime
def get_summary_generator(): 
    """Factory function to get the appropriate summary generator."""
    from app.config import settings
    
    use_llm = str(settings.USE_LLM).lower() == "true"
    
    # Rule-based generator 
    if not use_llm:
        return RuleBasedSummaryGenerator()
    
    # LLM-based generator
    api_key = settings.LLM_API_KEY
    
    if not api_key:
        print("Warning: USE_LLM is true but LLM_API_KEY is not set. Using rule-based summaries.")
        return RuleBasedSummaryGenerator()
    
    from app.ai.gemini_client import GeminiClient
    
    llm_client = GeminiClient(api_key)
    return LLMSummaryGenerator(llm_client)
