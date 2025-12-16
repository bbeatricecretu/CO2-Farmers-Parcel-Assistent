from fastapi import FastAPI
from app.storage.database import init_db # load Json files and create tables 
from app.api import manage #import router module

app = FastAPI(title="Farmers Parcel Assistant API")

@app.on_event("startup") #when fast api starts
def startup():
    init_db() 

app.include_router(manage.router) #takes routes defined in manage.py and mounts them to the app

@app.get("/") # verify that the API is running
def root():
    return {"message": "Farmers Parcel Assistant API is running"}
