from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#ORM models
Base = declarative_base()

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    
    parcels = relationship("Parcel", back_populates="farmer")

class Parcel(Base):
    __tablename__ = "parcels"
    
    id = Column(String, primary_key=True)
    farmer_id = Column(String, ForeignKey("farmers.id"), nullable=False)
    name = Column(String, nullable=False)
    area_ha = Column(Float, nullable=False)
    crop = Column(String, nullable=False)
    
    farmer = relationship("Farmer", back_populates="parcels")
    indices = relationship("ParcelIndex", back_populates="parcel")

class ParcelIndex(Base):
    __tablename__ = "parcel_indices"
    
    id = Column(String, primary_key=True)
    parcel_id = Column(String, ForeignKey("parcels.id"), nullable=False)
    date = Column(Date, nullable=False)
    ndvi = Column(Float, nullable=True)
    ndmi = Column(Float, nullable=True)
    ndwi = Column(Float, nullable=True)
    soc = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    ph = Column(Float, nullable=True)
    
    parcel = relationship("Parcel", back_populates="indices")

class FarmerReport(Base):
    __tablename__ = "farmer_reports"
    
    id = Column(String, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    report_frequency = Column(String, nullable=False)  # daily, weekly, or custom (e.g., "2 days")
    last_sent = Column(Date, nullable=True)  # Track when the last report was sent
