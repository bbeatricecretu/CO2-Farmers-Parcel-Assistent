"""LLM client for Google Gemini API."""
import warnings

# Suppress Google Generative AI deprecation warning
warnings.filterwarnings("ignore", message="All support for the `google.generativeai` package has ended", category=FutureWarning)

import google.generativeai as genai
from app.config import settings


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = None):
        """Initialize Gemini client with API key and model name."""
        if model_name is None:
            model_name = settings.LLM_MODEL
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
