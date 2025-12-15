from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.storage.db import get_db
from app.models.database import Farmer

router = APIRouter(tags=["message"])

# Intent detection
LIST_KEYWORDS = {"parcel", "parcels", "field", "fields"}
ACTION_KEYWORDS = {"show", "list", "see", "get", "what"}

def detect_intent(message):
    words = set(message.lower().split())
    
    if words & LIST_KEYWORDS and words & ACTION_KEYWORDS:
        return "LIST_PARCELS"
    
    return "UNKNOWN"

class MessageRequest(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

class MessageResponse(BaseModel):
    reply: str

class LinkRequest(BaseModel):
    phone: str
    username: str

class LinkResponse(BaseModel):
    reply: str

@router.post("/message", response_model=MessageResponse)
def message(payload: MessageRequest, db: Session = Depends(get_db)):
    # Check if phone number is already linked to a farmer
    farmer = db.query(Farmer).filter(Farmer.phone == payload.from_).first()
    
    if not farmer:
        # User is not linked - start onboarding
        reply = "Welcome! Please type your username to link your account."
    else:
        # User is linked - detect intent
        intent = detect_intent(payload.text)
        
        if intent == "LIST_PARCELS":
            # Get farmer's parcels
            parcels = farmer.parcels
            
            if parcels:
                parcel_list = "\n".join([
                    f"- {p.id}: {p.name} ({p.area_ha} ha, {p.crop})"
                    for p in parcels
                ])
                reply = f"Your parcels:\n{parcel_list}"
            else:
                reply = "You don't have any parcels registered."
        else:
            # Default response
            reply = f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."
    
    return {"reply": reply}

@router.post("/link", response_model=LinkResponse)
def link_account(payload: LinkRequest, db: Session = Depends(get_db)):
    # Check if username exists in database
    farmer = db.query(Farmer).filter(Farmer.username == payload.username).first()
    
    if not farmer:
        # Username not found - ask to try again
        reply = "Username not found. Please try again with a valid username."
    elif farmer.phone:
        # Username exists but already has a phone - error
        reply = "This account is already linked. Please try again with a different username."
    else:
        # Username found and no phone - link account
        farmer.phone = payload.phone
        db.commit()
        reply = f"Great, your account has been linked to {payload.phone}. You can now ask about your parcels."
    
    return {"reply": reply}
