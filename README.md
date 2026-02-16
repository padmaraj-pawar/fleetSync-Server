# FleetSync-Server

Enterprise-grade fleet tracking and analysis backend built with FastAPI.  
FleetSync-Server provides real-time ingestion, historical storage, analytics, and PDF reporting for fleet operations.

---

## 🚀 Infrastructure

The backend has migrated from local SQLite to **Supabase (PostgreSQL)** for cloud scalability.  
This enables horizontal scaling, managed backups, and production-grade reliability.

Connection configuration is managed via environment variables and consumed by `database.py` to initialize the SQLAlchemy engine.

---

## 📂 Project Structure

- `main.py` — FastAPI application and API endpoints  
- `models.py` — SQLAlchemy models (PostgreSQL compatible)  
- `database.py` — SQLAlchemy engine & session management  
- `.env` — (Local only) Private environment variables (Ignored by Git)  
- `test_db.py` — Database connectivity diagnostic script  
- `requirements.txt` — Python dependencies  

---

## ⚡ Quick Start

### 1️⃣ Environment Configuration

Create a `.env` file in the project root.

⚠ You must URL-encode special characters in your password.  
Example: Replace `@` with `%40`


---

### 2️⃣ Installation & Testing

Create a virtual environment, install dependencies, and verify the cloud connection.

#### Windows (PowerShell)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

## ✅ Verify Database Connection

```bash
python test_db.py
```

---

## 3️⃣ Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🗄 Database Schema (Models)

The production schema uses high-precision types and strict naming conventions defined in `models.py`.

### `models.Profile`

- Stores user and company details  
- Email, phone, and organization information  

### `models.Shipment`

- Telemetry and shipment history  
- `origin_lat`, `origin_long`: `Numeric(9,6)` for GPS precision  
- `co2_ermission`: Follows strict project naming specification (with 'r')  

**Status:**
- `1` = Pending  
- `2` = Active  
- `3` = Delivered  

### `models.TruckProfile`

- Vehicle and driver metadata  

---

## 🌐 API Endpoints

### Dashboard

#### `GET /dashboard/summary`
Fleet status and CO₂ trends  

#### `WS /dashboard/map/ws`
Live fleet position stream  

---

### Shipment

#### `GET /shipment/search/{truck_id}`
Real-time lookup for specific vehicles  

---

### Analysis

#### `GET /analysis/total-report`
Aggregated performance metrics  

#### `GET /analysis/generate-pdf`
Generates FPDF report with background cleanup  

---

### Notification (Ticketing)

#### `POST /notifications/create-batch`
Assigns shipments from ticket payloads  

---

### Settings

#### `GET /settings/config`
App-wide configurations (units, refresh rate, theme)  

---

### System & Diagnostics

#### `POST /ingest/pathway`
Real-time ingest for Pathway engine payloads  

#### `GET /test-db-insert`
Diagnostic route to verify write permissions on Supabase  

---

## 🔄 Real-time Ingest: `/ingest/pathway`

The ingest endpoint handles complex nested JSON payloads (GPS, ETA, Alerts).

### On Receive:

- Validates data via Pydantic models (`PathwayUpdate`)  
- Updates in-memory `fleet_state` for live WebSocket broadcasts  
- Persists historical snapshots to the PostgreSQL `shipment` table  

---

## 🔐 Notes

### Security
The `.env` file is ignored by Git to prevent credential leaks.

### Migrations
Tables are automatically created at startup via:

```python
models.Base.metadata.create_all()
```

### Dependencies

- `psycopg2-binary` — PostgreSQL driver  
- `python-dotenv` — Environment variable management  

---

## 🛠 Tech Stack

- FastAPI  
- SQLAlchemy  
- Supabase (PostgreSQL)  
- Uvicorn  
- FPDF  
- WebSockets  

---

## 👨‍💻 Author
fleetSync Backend Team
