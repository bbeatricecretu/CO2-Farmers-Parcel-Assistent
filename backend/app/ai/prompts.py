"""Prompt templates for LLM interactions."""


def get_intent_classification_prompt(user_message: str) -> str:
    return f"""You are an agricultural assistant helping farmers manage their parcels.
        Classify the user's intent from their message.

        User message: "{user_message}"

        Available intents:
        1. LIST_PARCELS - User wants to see all their parcels (e.g., "show my parcels", "what parcels do I have?", "List parcels")
        2. PARCEL_DETAILS - User wants details about a specific parcel (e.g., "tell me about parcel P1", "Tell me about parcel P1", "info about P1", "show details for P2")
        3. PARCEL_STATUS - User wants current status/health of a parcel (e.g., "how is P1 doing?", "is my field healthy?", "status of P1", "summary of P1")
        4. SET_REPORT_FREQUENCY - User wants to change how often they receive reports (e.g., "send reports weekly", "I want daily updates")
        5. UNKNOWN - Cannot determine clear intent

        Respond with ONLY the intent name(if are more choose one) (e.g., "LIST_PARCELS"). Do not include any explanation."""


def get_parcel_summary_prompt(
    parcel_id: str,
    parcel_name: str,
    indices: dict,
    interpretations: dict,
) -> str:
    """
    indices: raw numeric values (ndvi, ndmi, ndwi, nitrogen, ph, soc, etc.)
    interpretations: may contain metadata like 'date'
    """

    facts = []

    if indices.get("ndvi") is not None:
        facts.append(f"NDVI value: {indices['ndvi']:.2f}")

    if indices.get("ndmi") is not None:
        facts.append(f"NDMI value: {indices['ndmi']:.2f}")

    if indices.get("ndwi") is not None:
        facts.append(f"NDWI value: {indices['ndwi']:.2f}")

    if indices.get("nitrogen") is not None:
        facts.append(f"Nitrogen index: {indices['nitrogen']:.2f}")

    if indices.get("ph") is not None:
        facts.append(f"Soil pH: {indices['ph']:.2f}")

    if indices.get("soc") is not None:
        facts.append(f"Soil organic carbon: {indices['soc']:.2f}")

    last_date = interpretations.get("date", "an unknown date")
    facts.append(f"Measurement date: {last_date}")

    facts_text = "\n".join(f"- {fact}" for fact in facts)

    return f"""
You are an agricultural monitoring assistant.

Your task is to summarize parcel conditions based ONLY on the measured data below.

OUTPUT STRUCTURE (must follow):

1. Title line (neutral):
   Parcel {parcel_id} – {parcel_name} current status:

2. Bullet list:
   • 3–6 bullet points
   • Each bullet interprets ONE measurement
   • You may infer conditions (e.g., low, moderate, high)
   • Use simple, farmer-friendly language
   • Do NOT give advice or recommendations

3. Final line:
   A neutral conclusion referencing the measurement date ({last_date}).

IMPORTANT RULES:
- Do NOT invent measurements
- Do NOT give actions or recommendations
- Do NOT assume good or bad overall performance
- Interpretation must be cautious and data-driven
- Wording should be natural, not copied from input
- include measurement values in bullets
- rephrase each bullet in a unique way

MEASURED DATA:
{facts_text}

REFERENCE GUIDANCE (do not repeat verbatim):
- NDVI roughly reflects vegetation density (low < 0.3, moderate ~0.3–0.6, high > 0.6)
- NDMI relates to moisture availability
- NDWI reflects surface water presence
- Soil pH around 6–7 is typical for many crops

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
