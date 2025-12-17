# LLM Integration Guide

## Overview
This project supports optional LLM integration for generating natural language summaries of parcel reports. The system works with or without LLM enabled.

## Configuration

### 1. Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# Enable/Disable LLM
USE_LLM=false  # Set to 'true' to enable AI summaries

# LLM Provider
LLM_PROVIDER=gemini

# API Key
LLM_API_KEY=your_api_key_here
```

### 2. Get a Free Gemini API Key
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new project or select existing
4. Copy your API key
5. Add it to `.env` file

### 3. Install Dependencies
```bash
pip install google-generativeai
```

## How It Works

### Without LLM (Default)
- Uses rule-based summaries
- Fast and predictable
- No API calls or costs
- Example: "Parcel P1 is stable, good vegetation health, adequate moisture"

### With LLM Enabled
- Generates natural, conversational summaries
- More human-friendly language
- Adapts tone and phrasing
- Example: "Your North Field is looking great! The crops are healthy with good moisture levels."

### Fallback Safety
If LLM is enabled but fails (API error, rate limit, etc.), the system automatically falls back to rule-based summaries. Your application never breaks.

## Usage in Code

The factory pattern handles everything automatically:

```python
from app.ai.factory import get_summary_generator

# Automatically selects rule-based or LLM based on env
generator = get_summary_generator()

# Generate summary
summary = generator.generate_parcel_summary(parcel_id, indices_data)
```

## Cost Considerations

**Gemini Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for small to medium deployments

For production with many farmers, monitor your usage and consider:
- Caching summaries
- Rate limiting report generation
- Upgrading to paid tier if needed

## Testing

Run tests to verify both modes work:
```bash
# Test without LLM (default)
USE_LLM=false pytest

# Test with LLM (requires API key)
USE_LLM=true LLM_API_KEY=your_key pytest
```

## Architecture

```
ReportGenerationService
    ↓
get_summary_generator() (Factory)
    ↓
┌─────────────────────────────────┐
│  USE_LLM=false  │  USE_LLM=true │
├─────────────────┼───────────────┤
│ RuleBasedSummary│ LLMSummary    │
│ Generator       │ Generator     │
└─────────────────┴───────────────┘
```

The factory pattern ensures clean separation and easy testing of both approaches.
