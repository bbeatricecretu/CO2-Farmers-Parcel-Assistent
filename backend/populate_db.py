import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.storage.db import SessionLocal, init_db
from app.models.database import Farmer, Parcel, ParcelIndex

def load_json_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def populate_database():
    print("Initializing database...")
    init_db()
    
    db: Session = SessionLocal()
    
    try:
        print("Loading farmers...")
        farmers_data = load_json_file('data/farmers.json')
        for farmer_data in farmers_data:
            farmer = Farmer(
                id=farmer_data['id'],
                username=farmer_data['username'],
                name=farmer_data['name'],
                phone=farmer_data.get('phone')
            )
            db.add(farmer)
        db.commit()
        print(f"Loaded {len(farmers_data)} farmers")
        
        print("Loading parcels...")
        parcels_data = load_json_file('data/parcels.json')
        for parcel_data in parcels_data:
            parcel = Parcel(
                id=parcel_data['id'],
                farmer_id=parcel_data['farmer_id'],
                name=parcel_data['name'],
                area_ha=parcel_data['area_ha'],
                crop=parcel_data['crop']
            )
            db.add(parcel)
        db.commit()
        print(f"Loaded {len(parcels_data)} parcels")
        
        print("Loading parcel indices...")
        indices_data = load_json_file('data/parcel_indices.json')
        index_count = 0
        for parcel_id, indices in indices_data.items():
            for idx, index_data in enumerate(indices):
                index = ParcelIndex(
                    id=f"{parcel_id}_IDX{idx+1}",
                    parcel_id=parcel_id,
                    date=datetime.strptime(index_data['date'], '%Y-%m-%d').date(),
                    ndvi=index_data.get('ndvi'),
                    ndmi=index_data.get('ndmi'),
                    ndwi=index_data.get('ndwi'),
                    soc=index_data.get('soc'),
                    nitrogen=index_data.get('nitrogen'),
                    phosphorus=index_data.get('phosphorus'),
                    potassium=index_data.get('potassium'),
                    ph=index_data.get('ph')
                )
                db.add(index)
                index_count += 1
        db.commit()
        print(f"Loaded {index_count} parcel indices")
        
        print("Database populated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
