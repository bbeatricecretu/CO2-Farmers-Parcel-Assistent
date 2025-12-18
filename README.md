# CO2 Farmers Parcel Assistant

## 📋 What This Project Does

The **CO2 Farmers Parcel Assistant** is an intelligent chatbot system that helps farmers monitor and manage their agricultural parcels through conversational interactions. The system provides real-time insights about vegetation health, soil conditions, moisture levels, and crop trends based on satellite-derived indices.

**Key Features:**
- 💬 **Conversational Interface**: Natural language interaction for querying parcel information
- 📊 **Multi-Index Monitoring**: Tracks NDVI, NDMI, NDWI, Soil Organic Carbon, NPK nutrients, and pH levels
- 📈 **Trend Analysis**: Identifies improving, declining, or stable conditions over time
- 🤖 **AI-Powered Summaries**: Optional LLM integration for natural, human-friendly responses
- 📱 **WhatsApp-Ready Architecture**: Designed for easy integration with WhatsApp Business API
- ⏰ **Scheduled Reporting**: Configurable report frequencies (daily, weekly, custom)

---

## 🚀 Setup Instructions

### Prerequisites
- Python
- SQLite 
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CO2-Farmers-Parcel-Assistent
```

### 2. Set Up Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///farmers.sqlite

# LLM Configuration (Optional)
USE_LLM=false
LLM_PROVIDER=gemini
LLM_API_KEY=your_api_key_here
LLM_MODEL=gemini-1.5-flash
```

**To get a free Gemini API key:**
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create/select a project
3. Generate an API key
4. Set `USE_LLM=true` and add the key to `.env`

### 5. Initialize Database
The database is automatically populated from JSON files when the server starts for the first time. The data includes:
- 5 sample farmers
- 10+ parcels with different crops
- Historical parcel indices (NDVI, soil nutrients, etc.)

**To reload/reset the database:**
```bash
# Option 1: Delete the database file and restart the server
# (Database will be recreated automatically on next startup)
rm backend/farmers.sqlite
uvicorn app.main:app --reload

# Option 2: Manually run the population script
cd backend
python -c "from app.storage.populate_db import populate_db; populate_db()"
```

The JSON seed data files are located in `backend/data/`:
- `farmers.json` - Farmer accounts with usernames and phone numbers
- `parcels.json` - Parcel definitions (name, area, crop type)
- `parcel_indices.json` - Historical measurements (NDVI, nutrients, etc.)

---

## ▶️ How to Run the Project

### Start the API Server
```bash
cd backend
uvicorn app.main:app --reload
```

The server will start at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

### Run Tests
The project includes comprehensive tests for all services and repositories:

```bash
cd backend
python -m pytest -v
```

**Test Coverage:**
- ✅ Farmer service (account linking, retrieval)
- ✅ Parcel service (listing, details, status)
- ✅ Index service (data retrieval and analysis)
- ✅ Report service (frequency configuration)
- ✅ Trend analysis (multi-index trend detection)
- ✅ Repositories (database operations)

---

## 🔧 How to Test the Endpoints

### Using Postman
A complete Postman collection is included: **`CO2-Farmers-Parcel-Assistent.postman_collection.json`**

**Import Instructions:**
1. Open Postman
2. Click **Import** → **Upload Files**
3. Select `CO2-Farmers-Parcel-Assistent.postman_collection.json`
4. The collection includes all API endpoints with sample requests

**Available Endpoints:**

#### 1. Health Check
```
GET http://localhost:8000/
```

#### 2. Send Message (Chat Interface)
```
POST http://localhost:8000/message
Body:
{
  "from": "+40741111111",
  "text": "Show my parcels"
}
```

#### 3. Link Account
```
POST http://localhost:8000/link
Body:
{
  "phone": "+40741111111",
  "username": "ana.popescu"
}
```

**Sample Conversations:**
- `"Show my parcels"` → Lists all farmer's parcels
- `"Check status of P1"` → Shows current health status
- `"Get details for P1"` → Detailed indices and recommendations
- `"Set my report frequency to daily"` → Configures automated reports

### Using FastAPI Interactive Docs
Visit http://localhost:8000/docs for a Swagger UI where you can:
- Explore all endpoints
- Try requests interactively
- View request/response schemas

---

## 🏗️ Architecture & Project Structure

### High-Level Architecture
```
┌─────────────────┐
│  Chat Interface │ (WhatsApp/Postman)
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI API   │ (app/main.py)
└────────┬────────┘
         │
┌────────▼────────┐
│  Intent Service │ (Classifies user intent)
└────────┬────────┘
         │
    ┌────┴─────────────────┐
    │                      │
┌───▼──────┐      ┌────────▼─────┐
│ Services │      │  AI Factory  │
│  Layer   │◄─────┤ (LLM/Rules)  │
└────┬─────┘      └──────────────┘
     │
┌────▼──────────┐
│ Repositories  │ (Data Access)
└────┬──────────┘
     │
┌────▼──────────┐
│   Database    │ (SQLite)
└───────────────┘
```

### Directory Structure
```
CO2-Farmers-Parcel-Assistent/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── CO2-Farmers-Parcel-Assistent.postman_collection.json  # API tests
│
└── backend/
    ├── app/
    │   ├── main.py                    # FastAPI application entry point
    │   ├── config.py                  # Configuration & environment variables
    │   │
    │   ├── api/                       # API Layer
    │   │   ├── manage.py              # REST endpoints (/message, /link, /generate_reports)
    │   │   └── schemas.py             # Pydantic request/response models
    │   │
    │   ├── services/                  # Business Logic Layer
    │   │   ├── intent_service.py      # Message routing & intent detection
    │   │   ├── farmer_service.py      # Farmer account management
    │   │   ├── parcel_service.py      # Parcel queries & formatting
    │   │   ├── index_service.py       # Index data retrieval
    │   │   ├── report_service.py      # Report generation & scheduling
    │   │   └── trend_analysis_service.py  # Trend detection algorithms
    │   │
    │   ├── repositories/              # Data Access Layer
    │   │   ├── farmer_repo.py         # Farmer CRUD operations
    │   │   ├── parcel_repo.py         # Parcel CRUD operations
    │   │   ├── index_repo.py          # Index CRUD operations
    │   │   └── report_repo.py         # Report settings CRUD
    │   │
    │   ├── models/                    # Database Models
    │   │   └── base.py                # SQLAlchemy ORM models
    │   │
    │   ├── storage/                   # Database Layer
    │   │   ├── database.py            # Database connection & session management
    │   │   └── populate_db.py         # Initial data loading from JSON
    │   │
    │   └── ai/                        # AI/ML Layer
    │       ├── factory.py             # Factory pattern for AI components
    │       ├── intents.py             # Intent classification (rule-based & LLM)
    │       ├── summaries.py           # Summary generation (rule-based & LLM)
    │       ├── trends.py              # Trend summarization
    │       ├── prompts.py             # LLM prompt templates
    │       └── gemini_client.py       # Google Gemini API client
    │
    ├── data/                          # Seed Data
    │   ├── farmers.json               # Sample farmer accounts
    │   ├── parcels.json               # Sample parcels
    │   └── parcel_indices.json        # Historical index measurements
    │
    └── tests/                         # Test Suite
        ├── conftest.py                # Pytest fixtures
        ├── test_farmer_service.py
        ├── test_parcel_service.py
        ├── test_index_service.py
        ├── test_report_service.py
        ├── test_trend_analysis_service.py
        └── test_repositories.py
```

### Key Files Explained

#### **[backend/app/main.py](backend/app/main.py)**
FastAPI application entry point. Initializes the database on startup and registers API routes.

#### **[backend/app/config.py](backend/app/config.py)**
Configuration management using Pydantic Settings. Loads environment variables for database URL, LLM settings, and API keys.

#### **[backend/app/api/manage.py](backend/app/api/manage.py)**
Defines REST API endpoints:
- `POST /message` - Handles chat messages, returns structured responses
- `POST /link` - Links farmer accounts to phone numbers

#### **[backend/app/services/intent_service.py](backend/app/services/intent_service.py)**
Core message handler. Routes incoming messages through intent classification and delegates to appropriate services.

#### **[backend/app/services/trend_analysis_service.py](backend/app/services/trend_analysis_service.py)**
Analyzes temporal trends in parcel indices using a threshold-based algorithm (5% change detection).

#### **[backend/app/ai/factory.py](backend/app/ai/factory.py)**
Factory pattern implementation that provides the correct AI component (rule-based or LLM) based on configuration.

#### **[backend/app/ai/intents.py](backend/app/ai/intents.py)**
Intent classifiers:
- **RuleBasedIntentClassifier**: Keyword matching with regex
- **LLMIntentClassifier**: Uses Gemini API for context-aware classification

#### **[backend/app/ai/summaries.py](backend/app/ai/summaries.py)**
Summary generators:
- **RuleBasedSummaryGenerator**: Template-based summaries
- **LLMSummaryGenerator**: Natural language summaries via LLM

#### **[backend/app/models/base.py](backend/app/models/base.py)**
SQLAlchemy ORM models defining the database schema:
- `Farmer` - User accounts
- `Parcel` - Agricultural fields
- `ParcelIndex` - Time-series measurements
- `FarmerReport` - Report frequency settings

#### **[backend/app/storage/database.py](backend/app/storage/database.py)**
Database connection management, session factory, and automatic initialization from JSON seed data.

---

## 🔍 Rule-Based Analysis System

The system uses a sophisticated rule-based analysis approach for reliability and transparency:

### Intent Classification
**Keywords-based matching with priority:**

The classifier uses these keyword sets stored in memory:
- **LIST_KEYWORDS**: `{"parcels", "fields"}`
- **DETAIL_KEYWORDS**: `{"detail", "details", "about", "information", "info"}`
- **STATUS_KEYWORDS**: `{"how", "status", "summary", "condition", "health"}`
- **SET_KEYWORDS**: `{"set", "make", "change", "update"}`
- **REPORT_KEYWORDS**: `{"report", "reports", "frequency"}`
- **ACTION_KEYWORDS**: `{"show", "list", "see", "get", "what", "tell", "give"}`

**Intent Detection Logic:**
1. **SET_REPORT_FREQUENCY**: `SET_KEYWORDS ∩ (REPORT_KEYWORDS or "frequency")`
2. **PARCEL_STATUS**: `STATUS_KEYWORDS + Parcel ID (P\d+)`
3. **PARCEL_DETAILS**: `DETAIL_KEYWORDS + Parcel ID (P\d+)`
4. **LIST_PARCELS**: `LIST_KEYWORDS ∩ ACTION_KEYWORDS`

### Trend Analysis Algorithm
**5% Threshold-Based Detection:**
```python
change = (last_value - first_value) / first_value

if change > 0.05:    → "Increasing" ↗️
if change < -0.05:   → "Decreasing" ↘️
else:                → "Stable" →
```

**Applied to 8 indices:**
- **Vegetation**: NDVI (Normalized Difference Vegetation Index)
- **Moisture**: NDMI (Normalized Difference Moisture Index)
- **Water**: NDWI (Normalized Difference Water Index)
- **Soil Carbon**: SOC (Soil Organic Carbon)
- **Nutrients**: Nitrogen, Phosphorus, Potassium
- **Acidity**: pH

### Health Status Classification
```python
NDVI > 0.6:  "Healthy" ✅
NDVI 0.3-0.6: "Moderate" ⚠️
NDVI < 0.3:   "Poor" ❌
```

### Overall Parcel Status Assessment
The system counts how many indices are in good, moderate, or poor condition and provides an overall parcel status:

**Classification Thresholds (per index):**
- **NDVI**: Good ≥0.55 | Moderate 0.30-0.55 | Poor <0.30
- **NDMI**: Good >0.30 | Moderate 0.15-0.30 | Poor <0.15
- **NDWI**: Good >0.25 | Moderate 0.10-0.25 | Poor <0.10
- **SOC**: Good >2.5 | Moderate 1.5-2.5 | Poor <1.5
- **Nitrogen**: Good >1.0 | Moderate 0.7-1.0 | Poor <0.7
- **Phosphorus**: Good >0.45 | Moderate 0.35-0.45 | Poor <0.35
- **Potassium**: Good >0.7 | Moderate 0.55-0.7 | Poor <0.55
- **pH**: Good 6.0-7.0 | Moderate 5.5-6.0 or 7.0-7.5 | Poor <5.5 or >7.5

**Overall Status:**
- 🟢 **EXCELLENT**: ≥60% indices are good → "Continue current management practices"
- 🟡 **GOOD**: ≥70% indices are good or moderate → "Focus on improving moderate indices"
- 🟠 **MODERATE**: Mixed results → "Regular monitoring advised"
- 🔴 **NEEDS ATTENTION**: ≥50% indices are poor → "Immediate action required"

Each status includes a hardcoded recommendation for farmers to take appropriate action.

### Index-Specific Recommendations
Condition-based recommendations per index:
- Low NDVI → "Consider fertilization or irrigation"
- Low NDMI → "Monitor moisture, irrigation may be needed"
- Low Nitrogen → "Apply nitrogen-based fertilizer"
- High/Low pH → "Adjust soil pH with amendments"

---

## 🌟 Future Extensions

### 1. Real WhatsApp Integration

**Current State**: Mock phone-based interface via REST API

**Message Flow Architecture:**
```
Farmer
  |
  | WhatsApp message
  v
WhatsApp (Twilio / Meta)
  |
  | HTTP POST (webhook)
  v
YOUR FastAPI backend
  |
  | handle_message()
  v
Reply text
  |
  v
WhatsApp → Farmer
```

**Extension Plan:**
```python
# Use Twilio or WhatsApp Business API
from twilio.rest import Client

def receive_whatsapp_message(request):
    phone = request.form['From']
    message = request.form['Body']
    
    # Route to existing IntentService
    response = intent_service.handle_message(phone, message)
    
    # Send via Twilio
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=response,
        to=phone
    )
```

**Required Changes:**
- Add webhook endpoint in [manage.py](backend/app/api/manage.py)
- Install `twilio` package
- Register webhook URL with WhatsApp Business API
- Add authentication/security layer

---

### 2. Real Cron Jobs for Scheduled Reports

**Current State**: Report frequency stored but not scheduled

**Approach:**

Create a background task that runs daily at a predefined hour (e.g., 8 AM), queries the `farmer_reports` table in the database, and determines which farmers should receive reports today based on their last report date and configured frequency.

**Key Concepts:**

1. **Database-Driven Scheduling**
   - Store `last_sent_date` and `next_report_date` in `farmer_reports` table
   - Calculate `next_report_date` automatically based on frequency setting

2. **Frequency Calculation Logic**
   - `"daily"` → next_date = last_sent + 1 day
   - `"weekly"` → next_date = last_sent + 7 days
   - `"3 days"` → next_date = last_sent + 3 days


**Implementation File:**

```python
# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date

def send_scheduled_reports():
    """Background task: Check farmer_reports table and send due reports."""
    db = SessionLocal()
    
    try:
        # 1. Query database for farmers due for reports today
        today = date.today()
        farmers_due = report_repo.get_farmers_due_for_report(today)
        
        # 2. Generate reports for all due farmers
        reports = report_service.generate_reports_for_farmers(farmers_due)
        
        # 3. Send reports 
        ...
            
        # 4. Update last_sent_date and next_report_date in database
         report_repo.update_last_sent(report['phone'], today)
            
    except Exception as e:
        print(f"Error in scheduled report task: {e}")
    finally:
        db.close()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_scheduled_reports, 'cron', hour=8, minute=0)
scheduler.start()
```

**Integration into FastAPI:**
```python
# app/main.py
@app.on_event("startup")
def startup():
    init_db()
    scheduler.start()  # Start background scheduler

@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()  # Gracefully stop scheduler
```

**Required Changes:**
- **Database**: Add `last_sent_date` and `next_report_date` columns to `FarmerReport` model
- **Repository**: Add `get_farmers_due_for_report()` and `update_last_sent()` methods
- **Service**: Add `generate_reports_for_farmers()` batch method that iterates all farmers and their parcels
- **Scheduler**: Create `scheduler.py` with APScheduler configuration
- **Dependencies**: Install `apscheduler` package
- **Lifecycle**: Integrate scheduler start/stop into FastAPI events

---

### 3. Real TIFF Ingestion from Satellite Data

**Current State**: Static JSON data for indices

**Data Processing Pipeline:**

The TIFF ingestion follows this workflow using **PostGIS** for spatial operations:

```
pgsql

TIFF (satellite raster)
    ↓
Compute index per pixel
    ↓
Aggregate per parcel polygon
    ↓
Store numbers in DB 
```

**Conceptual Approach:**

1. **Import TIFF Files**
   - Store TIFF files in `backend/data/tiff/` directory
   - Organize by date: `2025-12-01_sentinel2.tif`
   - Each TIFF contains multiple bands (Red, NIR, SWIR, etc.)

2. **Compute Index per Pixel**
   - Load TIFF bands as numpy arrays
   - Apply index formulas pixel-by-pixel:
     - NDVI = (NIR - Red) / (NIR + Red)
     - NDMI = (NIR - SWIR) / (NIR + SWIR)
     - NDWI = (Green - NIR) / (Green + NIR)
   - Result: Index raster (same dimensions as input)

3. **Aggregate per Parcel Polygon**
   - Use parcel geometry
   - Extract pixels that fall within each parcel boundary
   - Calculate statistics: mean, median, std dev
   - Handle edge cases (partial pixels, no-data values)

4. **Store Numbers in Database**
   - Insert aggregated values into `parcel_indices` table
   - One row per parcel per date
   - Store as float values (not raster anymore)


**Usage:**
```python
# Manual TIFF loading
python -c "from app.storage.load_tiff import load_tiff_to_database; \
           load_tiff_to_database('backend/data/tiff/2025-12-01_sentinel2.tif', '2025-12-01')"
```

**Required Changes:**
- **Dependencies**: Install `GDAL`, `rasterio`, `shapely`, `numpy`
- **Storage**: Create `app/storage/load_tiff.py` module for TIFF processing
- **Data Directory**: Create `backend/data/tiff/` for storing satellite rasters

---

## 🤖 LLM & Database Integration

### LLM Integration Architecture

The system uses a **Factory Pattern** for seamless LLM integration with automatic fallback:

```
┌─────────────────┐
│  Configuration  │ (.env file)
└────────┬────────┘
         │
┌────────▼────────┐
│   AI Factory    │ (app/ai/factory.py)
└────────┬────────┘
         │
    ┌────┴─────────────────┐
    │                      │
┌───▼──────────┐   ┌───────▼────────┐
│ Rule-Based   │   │  LLM-Based     │
│ Components   │   │  Components    │
└──────────────┘   └────────────────┘
```

**Factory Functions:**
- `get_intent_classifier()` → Returns RuleBasedIntentClassifier or LLMIntentClassifier
- `get_summary_generator()` → Returns RuleBasedSummaryGenerator or LLMSummaryGenerator
- `get_trend_summarizer()` → Returns RuleBasedTrendSummarizer or LLMTrendSummarizer

**Configuration:**
```python
# config.py
class Settings(BaseSettings):
    USE_LLM: str = "false"           # Toggle LLM on/off
    LLM_PROVIDER: str = "gemini"     # Provider selection
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-flash"
```

**Factory Implementation:**
```python
# app/ai/factory.py
def get_summary_generator():
    if settings.USE_LLM.lower() == "true":
        try:
            client = GeminiClient(settings.LLM_API_KEY, settings.LLM_MODEL)
            return LLMSummaryGenerator(client)
        except Exception as e:
            print(f"LLM initialization failed: {e}")
            return RuleBasedSummaryGenerator()
    return RuleBasedSummaryGenerator()
```

**Benefits:**
- ✅ **Zero Code Changes**: Switch between modes via environment variable
- ✅ **Automatic Fallback**: Rules-based backup if LLM fails
- ✅ **Cost Control**: Disable LLM in dev, enable in production
- ✅ **Extensibility**: Easy to add new providers (OpenAI, Claude, etc.)

### Database Integration

**ORM Pattern with SQLAlchemy:**

1. **Models Layer** ([models/base.py](backend/app/models/base.py))
   - Defines database schema using SQLAlchemy ORM
   - Relationships: Farmer → Parcel → ParcelIndex

2. **Repository Layer** ([repositories/](backend/app/repositories/))
   - Encapsulates all database queries
   - Provides clean interface: `farmer_repo.get_by_phone(phone)`
   - Single responsibility per repository

3. **Service Layer** ([services/](backend/app/services/))
   - Business logic and orchestration
   - Combines multiple repositories
   - Applies rules and transformations

**Data Flow Example:**
```
User: "Check status of P1"
         ↓
IntentService.handle_message()
         ↓
ParcelService.get_parcel_status()
         ↓
ParcelRepository.get_by_id() ← Database Query
IndexRepository.get_latest_by_parcel() ← Database Query
         ↓
AI Factory → get_summary_generator()
         ↓
Response: "North Field (P1) is healthy..."
```

**Database Initialization:**
```python
# storage/database.py
def init_db():
    """Create tables and load seed data."""
    Base.metadata.create_all(bind=engine)
    
    if not db.query(Farmer).first():
        load_data_from_json()  # Populate from data/*.json
```

---

## 🚀 Future Development Roadmap

To scale this project to production, the following enhancements are planned:

### 1. Database Migration: SQLite → PostgreSQL
**Current**: SQLite for development simplicity  
**Future**: PostgreSQL with PostGIS extension

### 2. Cloud Hosting: Azure or AWS Deployment
**Current**: Local development server (localhost:8000)  
**Future**: Cloud-hosted production environment

### 3. WhatsApp Integration: Twilio → Meta WhatsApp Business API
**Current**: Mock REST API interface with phone numbers  
**Future**: Direct Meta WhatsApp Business API integration with webhooks

### 4. TIFF File Ingestion Pipeline
**Current**: Static JSON seed data for parcel indices  
**Future**: Automated satellite imagery processing with TIFF file ingestion

### 5. Cron Job Integration for Scheduled Reports
**Current**: Manual report requests via API  
**Future**: Automated daily/weekly report delivery with APScheduler background tasks

---

## 📧 Contact

**Email:** [cretu.beatricedenisa@gmail.com](mailto:cretu.beatricedenisa@gmail.com)  
**LinkedIn:** [linkedin.com/in/beatrice-cretu-551b6a380](https://www.linkedin.com/in/beatrice-cretu-551b6a380/)  
**GitHub:** [github.com/bbeatricecretu](https://github.com/bbeatricecretu)
