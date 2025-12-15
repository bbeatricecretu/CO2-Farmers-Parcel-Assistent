from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.storage.db import get_db
from app.models.database import Farmer

router = APIRouter(tags=["message"])

class MessageRequest(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

class MessageResponse(BaseModel):
    reply: str

@router.post("/message", response_model=MessageResponse)
def message(payload: MessageRequest, db: Session = Depends(get_db)):
    # Check if phone number is already linked to a farmer
    farmer = db.query(Farmer).filter(Farmer.phone == payload.from_).first()
    
    if farmer:
        # User is linked - respond normally
        reply = f"Hello {farmer.username}! Your account is linked. You can now ask about your parcels."
    else:
        # User is not linked - start onboarding
        reply = "Welcome! Please type your username to link your account."
    
    return {"reply": reply}
