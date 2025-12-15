from pydantic import BaseModel, Field

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

class ReportItem(BaseModel):
    to: str
    message: str

class GenerateReportsResponse(BaseModel):
    reports: list[ReportItem]
