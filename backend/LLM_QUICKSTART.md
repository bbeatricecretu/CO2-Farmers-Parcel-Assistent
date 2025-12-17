# Quick Start: LLM Integration

## Setup (Optional)

The project works perfectly without LLM. To enable AI-powered summaries:

### 1. Get Free Gemini API Key
Visit https://ai.google.dev/ and get your free API key.

### 2. Configure Environment
Create a `.env` file in the `backend/` directory:
```env
USE_LLM=true
LLM_PROVIDER=gemini
LLM_API_KEY=your_api_key_here
```

### 3. Install Dependencies
```bash
pip install google-generativeai
```

That's it! The system will now generate natural language summaries.

## Testing Both Modes

**Without LLM (default):**
```bash
USE_LLM=false pytest -v
```

**With LLM:**
```bash
USE_LLM=true LLM_API_KEY=your_key pytest -v
```

## Example Outputs

**Rule-based (default):**
> "Parcel P1 is stable, good vegetation health, adequate moisture, sufficient nitrogen, optimal pH"

**LLM-powered:**
> "Your North Field is looking great! The crops are healthy with strong vegetation and good water levels. Soil nutrients are well-balanced."

For more details, see [LLM_INTEGRATION.md](LLM_INTEGRATION.md)
