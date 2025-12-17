from pydantic import BaseModel, Field

#Pydantic DTO(Data Transfer Objects) schemas for request and response bodies

# /message
class MessageRequest(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

class MessageResponse(BaseModel):
    reply: str

class ParcelListItem(BaseModel):
    id: str
    name: str
    area: float
    crop: str

class ParcelListResponse(BaseModel):
    parcels: list[ParcelListItem]

class ParcelIndicesDetail(BaseModel):
    ndvi: float | None = None
    ndmi: float | None = None
    ndwi: float | None = None
    soc: float | None = None
    nitrogen: float | None = None
    phosphorus: float | None = None
    potassium: float | None = None
    ph: float | None = None

class ParcelDetailsResponse(BaseModel):
    parcel_id: str
    name: str
    area_ha: float
    crop: str
    data_date: str | None = None
    indices: ParcelIndicesDetail | None = None

# /link
class LinkRequest(BaseModel):
    phone: str
    username: str

class LinkResponse(BaseModel):
    reply: str

# /generate_report
class IndexDetail(BaseModel):
    value: float
    status: str

class ParcelIndices(BaseModel):
    ndvi: IndexDetail
    ndmi: IndexDetail
    ndwi: IndexDetail
    soc: IndexDetail
    n: IndexDetail
    p: IndexDetail
    k: IndexDetail
    ph: IndexDetail

class ParcelReportDetail(BaseModel):
    parcel_id: str
    name: str
    area_ha: float
    crop: str
    data_date: str
    indices: ParcelIndices
    summary: str

class ReportItem(BaseModel):
    to: str
    farmer: str
    report_type: str
    generated_at: str
    parcels: list[ParcelReportDetail]
