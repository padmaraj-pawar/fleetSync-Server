from sqlalchemy import func
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
import uvicorn, models, database, asyncio
from fpdf import FPDF
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
import os

# --- 1. DATA MODELS (PATHWAY CONTRACT) ---
class GPSData(BaseModel):
    lat: float; lon: float; speed_kmh: float; is_valid: bool

class ETAData(BaseModel):
    current_eta: str; baseline_eta: str; delay_minutes: int; confidence: float

class AlertData(BaseModel):
    alert_id: str; type: str; severity: str; details: Dict

class PathwayUpdate(BaseModel):
    update_timestamp: str; vehicle_id: str; shipment_id: str
    gps: GPSData; eta: ETAData; alerts: List[AlertData]

app = FastAPI(title="Tempo Enterprise System")
fleet_state: Dict[str, dict] = {} # Live Storage

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

# --- PAGE 1: DASHBOARD ---
@app.get("/dashboard/summary", tags=["1. Dashboard"])
def dashboard_summary():
    # Fleet Status & Efficiency logic
    active = len(fleet_state)
    delayed = sum(1 for v in fleet_state.values() if v['eta']['delay_minutes'] > 30)
    return {
        "co2_total_fleet": "5600 kg", # Placeholder for combined total
        "fleet_status": {"total": active, "delayed": delayed},
        "route_efficiency": "92%",
        "shipment_trends": [40, 55, 45, 70] # Day-wise
    }

@app.websocket("/dashboard/map/ws")
async def dashboard_map_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(list(fleet_state.values()))
        await asyncio.sleep(2)

@app.post("/dashboard/voice-ai", tags=["1. Dashboard"])
def voice_ai(query: str):
    return {"ai_response": f"Processing your request about: {query}"}

# --- PAGE 2: SHIPMENT ---
@app.get("/shipment/search/{truck_id}", tags=["2. Shipment"])
def shipment_search(truck_id: int, db: Session = Depends(get_db)):
    data = db.query(models.Shipment).filter(models.Shipment.truck_id == truck_id).first()
    if not data: return {"error": "Not Found"}
    return {
        "location": {"lat": data.origin_lat, "lon": data.origin_long},
        "load": data.load,
        "co2": data.co2_emission,
        "eta": "12:45 PM" # From live fleet_state in real app
    }

# --- PAGE 3: ANALYSIS ---
@app.get("/analysis/total-report", tags=["3. Analysis"])
def analysis_report(db: Session = Depends(get_db)):
    total_dist = db.query(func.sum(models.Shipment.distance_covered)).scalar() or 0
    return {
        "total_distance": f"{total_dist} km",
        "total_fleet_co2": "8900 kg",
        "available_fleet": 15,
        "pdf_url": "/analysis/generate-pdf"
    }

@app.get("/analysis/generate-pdf", tags=["3. Analysis"])
def generate_pdf(background_tasks: BackgroundTasks):
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="TEMPO FLEET ANALYSIS REPORT", ln=1, align='C')
    file = "report.pdf"
    pdf.output(file)
    background_tasks.add_task(os.remove, file)
    return FileResponse(file, filename=file)

# --- PAGE 4: NOTIFICATION (TICKETING) ---
@app.post("/notifications/create-batch", tags=["4. Notification"])
def create_batch(ticket: dict, db: Session = Depends(get_db)):
    # Maps ticketing data to the PDF 'Shipment' table
    new_s = models.Shipment(
        shipment_id=ticket.get("ticket_id"),
        truck_id=ticket.get("driver_id"),
        load=ticket.get("load"),
        status=1 # Initialized
    )
    db.add(new_s); db.commit()
    return {"status": "Ticket Assigned to Shipment Table"}

# --- PAGE 5: SETTINGS ---
@app.get("/settings/config", tags=["5. Settings"])
def get_settings():
    return {"units": "metric", "refresh_rate": "5s", "theme": "enterprise-dark"}

# --- IOT INGEST (PATHWAY) ---
@app.post("/ingest/pathway", tags=["System"])
async def ingest_pathway(data: PathwayUpdate, db: Session = Depends(get_db)):
    fleet_state[data.vehicle_id] = data.dict()
    # Update DB History
    db.query(models.Shipment).filter(models.Shipment.truck_id == data.vehicle_id).update({
        "avg_speed": data.gps.speed_kmh
    })
    db.commit()
    return {"status": "Live & DB Updated"}

# --- TEMPORARY DB TEST ROUTE ---
@app.get("/test-db-insert", tags=["System"])
def test_insert(db: Session = Depends(get_db)):
    try:
        # Create a dummy profile
        new_profile = models.Profile(
            emailid="test@college.edu",
            phoneNo=999991234,
            name="College PC Test",
            company_name="FleetSync Corp",
            company_address="123 Tech Campus"
        )
        
        # Add and commit
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        
        return {"status": "Success!", "data_inserted": new_profile.name}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)