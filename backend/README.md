# Farmers Parcel Assistant API

## Setup

1. Install PostgreSQL and create a database:
```bash
createdb farmers_db
```

2. Create a virtual environment and install dependencies:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure database connection:
- Copy `.env.example` to `.env`
- Update `DATABASE_URL` if needed

4. Populate the database:
```bash
python populate_db.py
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

6. Access the API:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- First endpoint: http://localhost:8000/manage/farmers

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── api/                 # API endpoints
│   │   └── manage.py        # Farmer management endpoints
│   ├── services/            # Business logic layer
│   │   ├── manage_farmer.py
│   │   └── parcel_service.py
│   ├── models/              # Database models
│   │   └── database.py
│   ├── repositories/        # Data access layer
│   │   ├── farmer_repo.py
│   │   ├── parcel_repo.py
│   │   └── index_repo.py
│   └── storage/
│       └── db.py            # Database connection
├── populate_db.py           # Database population script
└── requirements.txt
```
