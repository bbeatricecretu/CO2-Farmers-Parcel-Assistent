"""Factory for creating AI components."""
from app.ai.summaries import RuleBasedSummaryGenerator, LLMSummaryGenerator
from app.ai.intents import RuleBasedIntentClassifier, LLMIntentClassifier
from app.ai.trends import RuleBasedTrendSummarizer, LLMTrendSummarizer

def _get_llm_client():
    """Helper to get LLM client if configured."""
    from app.config import settings
    
    use_llm = str(settings.USE_LLM).lower() == "true"
    
    if not use_llm:
        return None
        
    api_key = settings.LLM_API_KEY
    if not api_key:
        print("Warning: USE_LLM is true but LLM_API_KEY is not set.")
        return None
        
    from app.ai.gemini_client import GeminiClient
    return GeminiClient(api_key, settings.LLM_MODEL)

def get_summary_generator(): 
    """Factory function to get the appropriate summary generator."""
    client = _get_llm_client()
    
    if client:
        return LLMSummaryGenerator(client)
    return RuleBasedSummaryGenerator()

def get_intent_classifier():
    """Factory function to get the appropriate intent classifier."""
    client = _get_llm_client()
    
    if client:
        return LLMIntentClassifier(client)
    return RuleBasedIntentClassifier()

def get_trend_summarizer():
    """Factory function to get the appropriate trend summarizer."""
    client = _get_llm_client()
    
    if client:
        return LLMTrendSummarizer(client)
    return RuleBasedTrendSummarizer()
