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
        response_text = intent_service.handle_message(clean_phone, message_body)
        
        # Convert dict response to string if needed
        if isinstance(response_text, dict):
            response_text = str(response_text)
        
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
    Webhook verification endpoint for Meta WhatsApp Business API.
    
    Meta requires a GET endpoint for webhook verification.
    Twilio doesn't need this, but we include it for future Meta migration.
    """
    # For Meta WhatsApp verification
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')
    
    # TODO: Add verification token to settings
    # verify_token = settings.META_WEBHOOK_VERIFY_TOKEN
    
    if mode == 'subscribe':
        # For now, just acknowledge
        logger.info("Webhook verification requested")
        return int(challenge) if challenge else {"status": "ok"}
    
    return {"status": "ok", "message": "Webhook endpoint active"}
