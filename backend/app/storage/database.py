from sqlalchemy import create_engine #doorway to the database
from sqlalchemy.orm import sessionmaker #machine that produces DB sessions
from app.config import settings
from app.models.base import Base #declarative base class

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30}
) #create single engine object  using the database URL from config
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal() #returns new Session object
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine) #metadata like an blueprint
