"""WhatsApp webhook endpoints for receiving messages from Twilio."""
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.storage.database import get_db
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])

# Lazy import to avoid blocking at module load time
def get_intent_service_lazy():
    from app.services.intent_service import IntentService
    return IntentService

def get_messenger_lazy():
    from app.services.messaging_service import get_messenger
    return get_messenger()


def format_whatsapp_message(data) -> str:
    """Format response data into a nice WhatsApp message."""
    # If already a string, check if it needs formatting
    if isinstance(data, str):
        # Format status messages that contain "Overall Status:"
        if "Overall Status:" in data:
            data = "📋 *Parcel Status Report*\n\n" + data
        # Format report frequency confirmation
        elif "report frequency has been set" in data.lower():
            data = "✅ " + data
        # Add emoji to error messages
        elif "not found" in data.lower() or "does not belong" in data.lower():
            data = "❌ " + data
        elif "No data available" in data:
            data = "⚠️ " + data
        elif "Invalid frequency" in data:
            data = "❌ " + data
        # Format welcome/help messages
        elif "Here are some things you can ask me" in data:
            data = "❓ " + data
        elif "Welcome!" in data or "Please type your username" in data:
            data = "👋 " + data
        return data
    
    # If it's a dict, format based on content
    if isinstance(data, dict):
        # Error messages
        if "error" in data:
            return f"❌ {data['error']}"
        
        # List of parcels
        if "parcels" in data:
            parcels = data["parcels"]
            if not parcels:
                return "You have no parcels registered."
            
            message = f"🌾 *Your Parcels* ({len(parcels)} total)\n\n"
            for p in parcels:
                message += f"📍 *{p['id']}* - {p['name']}\n"
                message += f"   {p['area']} ha • {p['crop']}\n\n"
            return message.strip()
        
        # Parcel details with indices
        if "parcel_id" in data and "indices" in data:
            msg = f"📊 *{data['parcel_id']} - {data['name']}*\n"
            msg += f"🌱 Crop: {data['crop']}\n"
            msg += f"📏 Area: {data['area_ha']} ha\n\n"
            
            if data['indices']:
                msg += f"📅 Data from: {data['data_date']}\n\n"
                indices = data['indices']
                msg += "*Vegetation Indices:*\n"
                if indices.get('ndvi'): msg += f"  NDVI: {indices['ndvi']}\n"
                if indices.get('ndmi'): msg += f"  NDMI: {indices['ndmi']}\n"
                if indices.get('ndwi'): msg += f"  NDWI: {indices['ndwi']}\n"
                
                msg += "\n*Soil Properties:*\n"
                if indices.get('soc'): msg += f"  SOC: {indices['soc']}%\n"
                if indices.get('nitrogen'): msg += f"  Nitrogen: {indices['nitrogen']} ppm\n"
                if indices.get('phosphorus'): msg += f"  Phosphorus: {indices['phosphorus']} ppm\n"
                if indices.get('potassium'): msg += f"  Potassium: {indices['potassium']} ppm\n"
                if indices.get('ph'): msg += f"  pH: {indices['ph']}\n"
            else:
                msg += "⚠️ No data available yet."
            
            return msg
    
    # Fallback: convert to string
    return str(data)


@router.post("/whatsapp")
async def receive_whatsapp_message(request: Request, db: Session = Depends(get_db)):
    """
    Webhook endpoint for receiving WhatsApp messages from Twilio.
    
    This endpoint is called by Twilio when a user sends a WhatsApp message.
    Configure this URL in your Twilio Console: https://your-domain.com/webhook/whatsapp
    
    For local development with ngrok:
    1. Run: ngrok http 8000
    2. Copy the ngrok URL (e.g., https://abc123.ngrok.io)
    3. Set Twilio webhook: https://abc123.ngrok.io/webhook/whatsapp
    """
    try:
        # Parse Twilio webhook data
        form_data = await request.form()
        
        # Extract message details
        from_number = form_data.get('From', '')  # Format: "whatsapp:+40741111111"
        message_body = form_data.get('Body', '')
        message_sid = form_data.get('MessageSid', '')
        
        logger.info(f"Received WhatsApp message from {from_number}: {message_body}")
        
        # Validate required fields
        if not from_number or not message_body:
            logger.error("Missing required fields in webhook data")
            raise HTTPException(status_code=400, detail="Missing From or Body")
        
        # Optional: Validate webhook signature (for production)
        if settings.MESSAGING_PROVIDER.lower() == "twilio" and settings.TWILIO_AUTH_TOKEN:
            messenger = get_messenger_lazy()
            is_valid = messenger.validate_webhook({
                'url': str(request.url),
                'signature': request.headers.get('X-Twilio-Signature', ''),
                'form_data': dict(form_data)
            })
            
            if not is_valid:
                logger.warning(f"Invalid webhook signature for message {message_sid}")
                # In production, you should reject invalid signatures
                # raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Clean phone number (remove 'whatsapp:' prefix)
        clean_phone = from_number.replace('whatsapp:', '')
        
        # Process message using existing intent service
        IntentService = get_intent_service_lazy()
        intent_service = IntentService(db)
        response_data = intent_service.handle_message(clean_phone, message_body)
        
        # Format response for WhatsApp
        response_text = format_whatsapp_message(response_data)
        
        logger.info(f"Generated response for {clean_phone}: {str(response_text)[:100]}...")
        
        # Return TwiML response so Twilio can send the message
        # This is the proper way for Twilio webhook responses
        from fastapi.responses import Response
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>'''
        
        return Response(content=twiml, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}", exc_info=True)
        # Return 200 to prevent Twilio from retrying
        return {"status": "error", "message": str(e)}


@router.get("/whatsapp")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint.
    
    Used for:
    - Testing webhook connectivity
    - Future Meta WhatsApp Business API integration (requires GET verification)
    
    Twilio doesn't require this endpoint.
    """
    return {"status": "ok", "message": "WhatsApp webhook endpoint is active"}
