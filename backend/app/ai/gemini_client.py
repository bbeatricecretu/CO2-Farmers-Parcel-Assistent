"""LLM client for Google Gemini API."""
import google.generativeai as genai


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
