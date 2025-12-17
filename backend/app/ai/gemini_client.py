"""LLM client for Google Gemini API."""
import google.generativeai as genai


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """Initialize Gemini client with API key and model name."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
