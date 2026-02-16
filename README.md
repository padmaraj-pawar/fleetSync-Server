# FleetSync-Server

Enterprise-grade fleet tracking and analysis backend built with FastAPI. FleetSync-Server provides real-time ingestion, historical storage, analytics and PDF reporting for fleet operations.

## Project Structure
- [main.py](main.py) — FastAPI application and API endpoints (see handlers like [`dashboard_summary`](main.py), [`shipment_search`](main.py), [`analysis_report`](main.py), [`generate_pdf`](main.py), [`create_batch`](main.py), [`get_settings`](main.py), [`ingest_pathway`](main.py)).
- [models.py](models.py) — SQLAlchemy models: [`models.Profile`](models.py), [`models.Shipment`](models.py), [`models.TruckProfile`](models.py).
- [database.py](database.py) — SQLAlchemy engine & session: [`database.engine`](database.py), [`database.SessionLocal`](database.py).
- [reuirements.txt](reuirements.txt) — Python dependencies.

## Quick Start

Create and activate a virtual environment, install dependencies, then run the app:

```bash
# Unix / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r reuirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r reuirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Features
- Real-time fleet state ingestion via a Pathway-compatible JSON contract.
- Historical storage in SQLite (tempo.db) via SQLAlchemy.
- Dashboard with WebSocket map updates.
- Shipment lookup and ticketing integration.
- Analysis endpoints with PDF report generation (FPDF).
- Simple settings and notification batch creation APIs.

## Database Schema (models)
Primary models are defined in [models.py](models.py).

- `models.Profile` — user/company profile (fields: `emailid`, `phoneNo`, `name`, `company_name`, `company_address`). See [`models.Profile`](models.py).

- `models.Shipment` — shipment history and telemetry (see [`models.Shipment`](models.py])):
  - `shipment_id` (Integer, PK)
  - `origin_lat`, `origin_long` (Numeric(9,6)) — origin GPS coordinates
  - `destination_lat`, `destination_long` (Numeric(9,6)) — destination GPS coordinates
  - `truck_id` (Integer) — associated vehicle
  - `load` (Numeric) — cargo/load metric
  - `status` (Integer) — 1=Pending, 2=Active, 3=Delivered
  - `co2_emission` (String(10)) — recorded CO₂ metric (string formatted)
  - `avg_speed` (Float) — average speed snapshot
  - `distance_covered` (Float) — accumulated distance
  - Model source: [`models.Shipment`](models.py)

- `models.TruckProfile` — truck/driver contact and status (fields: `truck_id`, `email_id`, `phone_no`, `name`, `company_name`, `active_status`). See [`models.TruckProfile`](models.py).

## API Endpoints (grouped by pages)
Handlers and route implementations live in [main.py](main.py). Referenced function symbols are linked below.

1. Dashboard
- GET `/dashboard/summary` — [`dashboard_summary`](main.py) — fleet status, CO₂ summary, trends.
- WebSocket `/dashboard/map/ws` — [`dashboard_map_ws`](main.py) — pushes live fleet positions.
- POST `/dashboard/voice-ai` — [`voice_ai`](main.py) — simple voice-AI placeholder.

2. Shipment
- GET `/shipment/search/{truck_id}` — [`shipment_search`](main.py) — look up shipment by truck_id (returns location, load, CO₂, ETA).

3. Analysis
- GET `/analysis/total-report` — [`analysis_report`](main.py) — aggregated metrics and link to PDF.
- GET `/analysis/generate-pdf` — [`generate_pdf`](main.py) — generates a PDF report using FPDF (dependency: `fpdf2` in [reuirements.txt](reuirements.txt)).

4. Notification (Ticketing)
- POST `/notifications/create-batch` — [`create_batch`](main.py) — creates/assigns shipment records from ticket payloads.

5. Settings
- GET `/settings/config` — [`get_settings`](main.py) — returns app settings (units, refresh rate, theme).

System / Integrations
- POST `/ingest/pathway` — [`ingest_pathway`](main.py) — real-time ingest route for Pathway engine payloads.

## Real-time Ingest: /ingest/pathway
The ingest endpoint expects a nested JSON payload that conforms to the Pydantic contract defined in [main.py](main.py):
- [`GPSData`](main.py) — lat, lon, speed_kmh, is_valid
- [`ETAData`](main.py) — current_eta, baseline_eta, delay_minutes, confidence
- [`AlertData`](main.py) — alert_id, type, severity, details
- [`PathwayUpdate`](main.py) — update_timestamp, vehicle_id, shipment_id, gps, eta, alerts

When a POST is received at `/ingest/pathway`, the server:
1. Validates/parses nested JSON into the [`PathwayUpdate`](main.py) model.
2. Updates in-memory `fleet_state` (live storage) for WebSocket/dashboard consumption (see `fleet_state` in [main.py](main.py)).
3. Persists summary values to the `shipment` table via SQLAlchemy (e.g., `avg_speed` update).
See implementation: [`ingest_pathway`](main.py).

## PDF Reporting
Analysis reports are generated using FPDF in [`generate_pdf`](main.py). The endpoint writes a temporary `report.pdf`, serves it as a `FileResponse`, and schedules removal via `BackgroundTasks`. Dependency for PDF generation is `fpdf2` (listed in [reuirements.txt](reuirements.txt)).

## Database & Migrations
- SQLite file: `tempo.db` (ignored by .gitignore).
- SQLAlchemy Base is exposed via [`database.Base`](database.py) and tables are created at startup in [main.py](main.py) using `models.Base.metadata.create_all(bind=database.engine)`.

## Notes
- This repository uses a simple SQLite backend for demonstration and local development. For production, replace `database.SQLALCHEMY_DATABASE_URL` with a production-grade RDBMS and add migrations.
- Endpoints include placeholders and simplified logic intended as a scaffold for enterprise workflows.

If you need the README adjusted (shorter/longer or with additional sections like deployment or tests), I can update it.