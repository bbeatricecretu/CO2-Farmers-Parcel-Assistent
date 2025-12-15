from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.storage.database import get_db
from app.services.chat_service import ChatService
from app.services.farmer_service import FarmerService
from app.services.report_generation_service import ReportGenerationService
from app.api.schemas import MessageRequest, MessageResponse, LinkRequest, LinkResponse, GenerateReportsResponse, ReportItem

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

@router.post("/generate-reports", response_model=list[ReportItem])
def generate_reports(db: Session = Depends(get_db)):
    report_service = ReportGenerationService(db)
    reports = report_service.generate_reports()
    return reports
