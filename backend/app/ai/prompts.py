"""Prompt templates for LLM interactions."""


def get_intent_classification_prompt(user_message: str) -> str:
    return f"""You are an agricultural assistant helping farmers manage their parcels.
        Classify the user's intent from their message.

        User message: "{user_message}"

        Available intents:
        1. LIST_PARCELS - User wants to see all their parcels (e.g., "show my parcels", "what parcels do I have?", "list fields")
        2. PARCEL_DETAILS - User wants details about a specific parcel (e.g., "tell me about parcel P1", "details of North Field", "info about P1")
        3. PARCEL_STATUS - User wants current status/health of a parcel (e.g., "how is P1 doing?", "is my field healthy?", "status of P1", "summary of P1")
        4. SET_REPORT_FREQUENCY - User wants to change how often they receive reports (e.g., "send reports weekly", "I want daily updates")
        5. UNKNOWN - Cannot determine clear intent

        Respond with ONLY the intent name (e.g., "LIST_PARCELS"). Do not include any explanation."""


def get_parcel_summary_prompt(
    parcel_id: str,
    parcel_name: str,
    indices: dict,
    interpretations: dict,
) -> str:
    facts = []

    # Extract date safely (expected to be passed in indices)
    last_date = indices.get("date", "an unknown date")

    if indices.get("ndvi") is not None:
        facts.append(
            f"NDVI is approximately {indices['ndvi']:.2f}, "
            f"which indicates {interpretations.get('vegetation', 'an unclear vegetation condition')}."
        )

    if indices.get("ndmi") is not None:
        facts.append(
            f"NDMI is around {indices['ndmi']:.2f}, "
            f"suggesting {interpretations.get('moisture', 'uncertain soil moisture conditions')}."
        )

    if indices.get("ph") is not None:
        facts.append(
            f"Soil pH is close to {indices['ph']:.1f}, "
            f"described as {interpretations.get('ph', 'not clearly classified')}."
        )

    if indices.get("nitrogen") is not None:
        facts.append(
            f"Nitrogen levels are considered {interpretations.get('nitrogen', 'unknown')}."
        )

    if indices.get("soc") is not None:
        facts.append(
            f"Soil organic carbon levels appear {interpretations.get('soc', 'unknown')}."
        )

    facts_text = "\n".join(f"- {fact}" for fact in facts)

    return f"""
You are an agricultural assistant generating a parcel STATUS SUMMARY for a farmer.

OUTPUT STRUCTURE (must follow):

1. Title line (neutral, factual):
Parcel {parcel_id} – {parcel_name} current status:

2. Bullet list:
• 3–6 bullet points
• Each bullet describes one important observation
• You may paraphrase freely
• Use simple, farmer-friendly language
• Mention values when relevant

3. Final line:
A short neutral conclusion that explicitly mentions the measurement date ({last_date}).

IMPORTANT RULES:
- Keep the structure exactly (title → bullets → final line)
- Do NOT copy the input text verbatim
- Do NOT invent data or recommendations
- Do NOT assume good or bad conditions
- Use your own wording while staying factual

FACTS AND INTERPRETATIONS:
{facts_text}

OUTPUT:
"""





def get_trend_analysis_summary_prompt(parcel_id: str, parcel_name: str, trends: dict) -> str:
    # Build trend information
    trend_info = []
    
    for index_name, data in trends.items():
        if isinstance(data, dict) and "trend" in data:
            trend = data["trend"]
            explanation = data.get("recommendation", "")
            first_val = data.get("first_value", 0)
            last_val = data.get("last_value", 0)
            
            trend_emoji = "📈" if trend == "increasing" else "📉" if trend == "decreasing" else "➡️"
            trend_info.append(f"{trend_emoji} {index_name.upper()}: {trend} (from {first_val:.2f} to {last_val:.2f})")
            if explanation:
                trend_info.append(f"   → {explanation}")
    
    trends_text = "\n".join(trend_info) if trend_info else "No trend data available"
    
    return f"""You are an agricultural assistant creating a friendly trend analysis summary for a farmer.
        Parcel: {parcel_name} ({parcel_id})
        Trend Analysis:
        {trends_text}

        Create a brief (2-4 sentences) natural language summary of how the parcel is changing over time.
        - Be conversational and friendly
        - Focus on the most significant trends
        - Explain what the trends mean in simple terms
        - Keep it concise and actionable
        - Do not repeat technical values, just describe the patterns

        Example style: "Over the past period, your North Field shows improving vegetation health with steady moisture levels. Soil nutrients are gradually depleting, which is normal as crops consume them. Overall, the field is healthy but keep an eye on nitrogen levels."

        Summary:"""
