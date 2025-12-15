from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.storage.db import get_db
from app.services.chat_service import ChatService
from app.services.farmer_service import FarmerService
from app.api.schemas import MessageRequest, MessageResponse, LinkRequest, LinkResponse

router = APIRouter(tags=["message"])

@router.post("/message", response_model=MessageResponse)
def message(payload: MessageRequest, db: Session = Depends(get_db)):
    chat_service = ChatService(db)
    reply = chat_service.handle_message(payload.from_, payload.text)
    return {"reply": reply}

@router.post("/link", response_model=LinkResponse)
def link_account(payload: LinkRequest, db: Session = Depends(get_db)):
    farmer_service = FarmerService(db)
    reply = farmer_service.link_account(payload.phone, payload.username)
    return {"reply": reply}
