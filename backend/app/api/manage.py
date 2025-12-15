from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["message"])

class MessageRequest(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

class MessageResponse(BaseModel):
    reply: str

@router.post("/message", response_model=MessageResponse)
def message(payload: MessageRequest):
    return {"reply": "Your response message as text"}
