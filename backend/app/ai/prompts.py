"""Prompt templates for LLM interactions."""


def get_intent_classification_prompt(user_message: str) -> str:
    """
    Prompt for classifying user intent from their message.
    
    Returns one of:
    - LIST_PARCELS: User wants to see all their parcels
    - PARCEL_DETAILS: User wants details about a specific parcel
    - PARCEL_STATUS: User wants current status of a parcel
    - SET_REPORT_FREQUENCY: User wants to change report frequency
    - UNKNOWN: Cannot determine intent
    """
    return f"""You are an agricultural assistant helping farmers manage their parcels.
Classify the user's intent from their message.

User message: "{user_message}"

Available intents:
1. LIST_PARCELS - User wants to see all their parcels (e.g., "show my parcels", "what parcels do I have?", "list fields")
2. PARCEL_DETAILS - User wants details about a specific parcel (e.g., "tell me about parcel P1", "status of North Field")
3. PARCEL_STATUS - User wants current status/health of a parcel (e.g., "how is P1 doing?", "is my field healthy?")
4. SET_REPORT_FREQUENCY - User wants to change how often they receive reports (e.g., "send reports weekly", "I want daily updates")
5. UNKNOWN - Cannot determine clear intent

Respond with ONLY the intent name (e.g., "LIST_PARCELS"). Do not include any explanation."""


def get_parcel_summary_prompt(parcel_id: str, parcel_name: str, indices: dict, interpretations: dict) -> str:
    """
    Prompt for generating natural language parcel summary.
    
    Args:
        parcel_id: Parcel identifier (e.g., "P1")
        parcel_name: Human-readable parcel name (e.g., "North Field")
        indices: Dictionary of index values (ndvi, ndmi, nitrogen, etc.)
        interpretations: Dictionary of rule-based interpretations for each index
    """
    # Build index information string
    index_info = []
    
    if indices.get("ndvi") is not None:
        status = interpretations.get("vegetation", "")
        index_info.append(f"- Vegetation (NDVI: {indices['ndvi']:.2f}): {status}")
    
    if indices.get("ndmi") is not None:
        status = interpretations.get("moisture", "")
        index_info.append(f"- Moisture (NDMI: {indices['ndmi']:.2f}): {status}")
    
    if indices.get("ndwi") is not None:
        status = interpretations.get("water", "")
        index_info.append(f"- Water Content (NDWI: {indices['ndwi']:.2f}): {status}")
    
    if indices.get("nitrogen") is not None:
        status = interpretations.get("nitrogen", "")
        index_info.append(f"- Nitrogen: {indices['nitrogen']:.2f} - {status}")
    
    if indices.get("phosphorus") is not None:
        status = interpretations.get("phosphorus", "")
        index_info.append(f"- Phosphorus: {indices['phosphorus']:.2f} - {status}")
    
    if indices.get("potassium") is not None:
        status = interpretations.get("potassium", "")
        index_info.append(f"- Potassium: {indices['potassium']:.2f} - {status}")
    
    if indices.get("ph") is not None:
        status = interpretations.get("ph", "")
        index_info.append(f"- pH Level: {indices['ph']:.2f} - {status}")
    
    if indices.get("soc") is not None:
        status = interpretations.get("soc", "")
        index_info.append(f"- Soil Organic Carbon: {indices['soc']:.2f} - {status}")
    
    indices_text = "\n".join(index_info) if index_info else "No data available"
    
    return f"""You are an agricultural assistant creating a friendly, conversational summary for a farmer.

Parcel: {parcel_name} ({parcel_id})
Current Measurements and Status:
{indices_text}

Create a brief (2-3 sentences) natural language summary for the farmer. 
- Be conversational and friendly
- Highlight the most important information
- Mention any concerns or positive aspects
- Use simple language, avoid technical jargon
- Do not make specific recommendations, just describe the current state

Example style: "Your North Field is looking healthy! The crops have good vegetation density and adequate moisture levels. Soil nutrients are well-balanced with good nitrogen and pH levels."

Summary:"""


def get_trend_analysis_summary_prompt(parcel_id: str, parcel_name: str, trends: dict) -> str:
    """
    Prompt for generating natural language trend analysis summary.
    
    Args:
        parcel_id: Parcel identifier
        parcel_name: Human-readable parcel name
        trends: Dictionary of trend data for each index with trend direction and explanation
    """
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
