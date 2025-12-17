from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union
from app.storage.database import get_db
from app.services.intent_service import IntentService
from app.services.farmer_service import FarmerService
from app.services.report_service import ReportService
from app.services.trend_analysis_service import TrendAnalysisService
from app.api.schemas import MessageRequest, MessageResponse, LinkRequest, LinkResponse, ReportItem, ParcelListResponse, ParcelDetailsResponse

router = APIRouter(tags=["message"])

@router.post("/message", response_model=Union[MessageResponse, ParcelListResponse, ParcelDetailsResponse])
def message(payload: MessageRequest, db: Session = Depends(get_db)):
    intent_service = IntentService(db)
    reply = intent_service.handle_message(payload.from_, payload.text)
    
    # If reply is a dict (structured response), return it directly
    if isinstance(reply, dict):
        return reply
    
    # Otherwise, wrap string reply in MessageResponse
    return {"reply": reply}

@router.post("/link", response_model=LinkResponse)
def link_account(payload: LinkRequest, db: Session = Depends(get_db)):
    farmer_service = FarmerService(db)
    reply = farmer_service.link_account(payload.phone, payload.username)
    return {"reply": reply}

@router.post("/generate-reports", response_model=list[ReportItem])
def generate_reports(db: Session = Depends(get_db)):
    report_service = ReportService(db)
    reports = report_service.generate_reports()
    return reports

@router.get("/parcel/{parcel_id}/trends")
def get_parcel_trends(parcel_id: str, db: Session = Depends(get_db)):
    """
    Analyze trends for a parcel's indices over time.
    
    - **parcel_id**: The parcel identifier
    
    Returns trend analysis showing if indices are increasing, decreasing, or stable.
    Uses standard thresholds optimized for each index type.
    """
    trend_service = TrendAnalysisService(db)
    trends = trend_service.analyze_parcel_trends(parcel_id)
    
    if trends.get("status") == "insufficient_data":
        raise HTTPException(status_code=400, detail=trends["message"])
    
    return trends
