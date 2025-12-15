from sqlalchemy.orm import Session
from app.models.database import ParcelIndex

class IndexRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_parcel_id(self, parcel_id: str):
        return self.db.query(ParcelIndex).filter(ParcelIndex.parcel_id == parcel_id).all()
    
