from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.storage.db import get_db
from app.services.message_service import MessageService

router = APIRouter(tags=["message"])

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
    message_service = MessageService(db)
    reply = message_service.handle_message(payload.from_, payload.text)
    return {"reply": reply}

@router.post("/link", response_model=LinkResponse)
def link_account(payload: LinkRequest, db: Session = Depends(get_db)):
    message_service = MessageService(db)
    reply = message_service.link_account(payload.phone, payload.username)
    return {"reply": reply}
