from pydantic import BaseModel, Field

#Pydantic DTO(Data Transfer Objects) schemas for request and response bodies

# /message
class MessageRequest(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

class MessageResponse(BaseModel):
    reply: str

# /link
class LinkRequest(BaseModel):
    phone: str
    username: str

class LinkResponse(BaseModel):
    reply: str

# /generate_report
class ReportItem(BaseModel):
    to: str
    message: str

class GenerateReportsResponse(BaseModel):
    reports: list[ReportItem]
