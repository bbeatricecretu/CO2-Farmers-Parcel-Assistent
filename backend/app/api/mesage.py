from pydantic import BaseModel

class MessageRequest(BaseModel):
    from_: str
    text: str

class MessageResponse(BaseModel):
    reply: str
