from sqlalchemy import func
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
import uvicorn, models, database, asyncio
from fpdf import FPDF
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks # Update this at the top
import os

app = FastAPI(title="Tempo Enterprise System")

# Ensure tables are created
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

# --- 1. DASHBOARD PAGE ---
@app.get("/dashboard/summary", tags=["1. Dashboard"])
def get_dashboard_summary(db: Session = Depends(get_db)):
    # 1. Calculate Total CO2 from all entries in the database
    total_co2 = db.query(func.sum(models.Telemetry.co2_emitted)).scalar() or 0
    
    # 2. Count Active Trucks
    active_count = db.query(models.Telemetry.tempo_id).distinct().count()
    
    return {
        "co2_total_fleet": round(total_co2, 2),
        "route_efficiency_score": 92.5, # We will calculate this later
        "fleet_status": {"total": active_count, "on_road": active_count, "maintenance": 0},
        "shipment_trends": {"labels": ["Mon", "Tue", "Wed"], "data": [120, 150, 110]}
    }

@app.websocket("/dashboard/map/ws")
async def dashboard_map_ws(websocket: WebSocket):
    """INCLUDES: MAP (Live moving vehicle details)"""
    await websocket.accept()
    while True:
        await websocket.send_json({"tempo_id": "T-01", "lat": 19.07, "lon": 72.87, "status": "Moving"})
        await asyncio.sleep(5)

@app.post("/dashboard/voice-ai", tags=["1. Dashboard"])
def voice_ai_interaction(query: str, db: Session = Depends(get_db)):
    """
    PROVISION: This route is the gateway for the Team Leader's Voice Model.
    It currently simulates the 'Brain' logic.
    """
    # 1. We fetch real data so the AI can 'know' the fleet status
    active_trucks = db.query(models.Telemetry.tempo_id).distinct().count()
    total_co2 = db.query(func.sum(models.Telemetry.co2_emitted)).scalar() or 0
    
    # 2. Simulated 'Brain' Logic (This is where the TL's model will eventually plug in)
    if "status" in query.lower():
        response_text = f"Currently, there are {active_trucks} trucks active on the map."
    elif "co2" in query.lower() or "emission" in query.lower():
        response_text = f"The total fleet emissions are {round(total_co2, 2)} kilograms."
    else:
        response_text = "I am connected and monitoring the Tempo fleet. How can I help?"

    return {
        "input_query": query,
        "ai_response_text": response_text,
        "status": "Voice Model Provision Active"
    }

# --- 2. SHIPMENT PAGE ---
@app.get("/shipment/search/{truck_id}", tags=["2. Shipment"])
def search_truck_details(truck_id: str, db: Session = Depends(get_db)):
    # Look for the LATEST data for this specific truck
    truck_data = db.query(models.Telemetry).filter(models.Telemetry.tempo_id == truck_id).order_by(models.Telemetry.id.desc()).first()
    
    if not truck_data:
        return {"error": "Truck not found in live fleet. Try Tempo-01"}
        
    return {
        "truck_id": truck_data.tempo_id,
        "location": {"lat": truck_data.latitude, "lon": truck_data.longitude},
        "load": f"{truck_data.load_weight}kg",
        "co2": f"{truck_data.co2_emitted}kg",
        "eta": "10:30 AM" 
    }

# --- 3. ANALYSIS PAGE ---
@app.get("/analysis/total-report", tags=["3. Analysis"])
def get_fleet_analysis_report():
    """
    INCLUDES:
    - Route Efficiency (Combined)
    - Total Available Fleet
    - Shipment Trends (Day-wise)
    - Total Distance & Total CO2
    - PDF Generation Trigger
    """
    return {
        "combined_efficiency": "89%",
        "available_fleet": 20,
        "total_distance_covered": "12,400 km",
        "total_co2_emission": "5600 kg",
        "trends": [45, 55, 40, 70],
        "pdf_export_url": "/api/v1/generate-pdf"
    }

@app.get("/analysis/generate-pdf", tags=["3. Analysis"])
def generate_fleet_report(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Pull stats from the database
    total_telemetry = db.query(models.Telemetry).count()
    total_tickets = db.query(models.DeliveryTicket).count()
    
    # 2. Create the PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "TEMPO ENTERPRISE - FLEET REPORT", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total Live Movement Records: {total_telemetry}", ln=True)
    pdf.cell(0, 10, f"Total Active Delivery Tickets: {total_tickets}", ln=True)
    pdf.cell(0, 10, "Status: Fleet Performance Optimal", ln=True)
    
    # 3. Save it to a temporary file
    file_name = "fleet_analysis.pdf"
    pdf.output(file_name)
    
    # --- OPTION 1 LOGIC ---
    # This tells FastAPI: "Wait until the user finishes downloading, then delete the file"
    background_tasks.add_task(os.remove, file_name)
    
    # 4. Send the file to the browser
    return FileResponse(path=file_name, filename=file_name, media_type='application/pdf')

# --- 4. NOTIFICATION PAGE ---
@app.post("/notifications/create-batch", tags=["4. Notification"])
def create_notification_batch(ticket: dict, db: Session = Depends(get_db)):
    """
    INCLUDES:
    - customer_id, ticket_id, origin, destination, load, driver_id
    """
    new_notif = models.DeliveryTicket(
        ticket_id=ticket.get("ticket_id"),
        customer_id=ticket.get("customer_id"),
        origin=ticket.get("origin"),
        destination=ticket.get("destination"),
        load_type=ticket.get("load"),
        driver_id=ticket.get("driver_id")
    )
    db.add(new_notif)
    db.commit()
    return {"status": "Batch Created", "ticket_id": ticket.get("ticket_id")}


# --- 5. SETTINGS PAGE ---
# Initial "Mock" settings (In a real app, these would be in a DB table)
app_settings = {
    "distance_unit": "km",
    "weight_unit": "kg",
    "map_refresh_rate": 5, # seconds
    "notification_sound": True,
    "language": "English"
}

@app.get("/settings/config", tags=["5. Settings"])
def get_settings():
    """Returns the current system configuration"""
    return app_settings

@app.post("/settings/update-config", tags=["5. Settings"])
def update_config(unit: str = "km", refresh_rate: int = 5, language: str = "English"):
    """
    Standard Industry Settings:
    Updates system-wide preferences for distance units and UI behavior.
    """
    app_settings["distance_unit"] = unit
    app_settings["map_refresh_rate"] = refresh_rate
    app_settings["language"] = language
    
    return {
        "status": "Configuration Updated",
        "applied_settings": app_settings
    }

# --- CATEGORY C: SYSTEM/IOT DOMAIN ---
@app.post("/telemetry/ingest", tags=["System/IoT Domain"])
def ingest_telemetry(data: dict, db: Session = Depends(get_db)):
    """
    This is the 'Gate'. The simulator sends data here.
    It takes lat, lon, temp, and co2 from the simulator.
    """
    new_entry = models.Telemetry(
        tempo_id=data.get("tempo_id"),
        latitude=data.get("lat"),
        longitude=data.get("lon"),
        temperature=data.get("temp"),
        co2_emitted=data.get("co2", 0.0),
        load_weight=data.get("load", 0.0)
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"status": "Successfully Saved", "database_id": new_entry.id}

@app.get("/health", tags=["System/IoT Domain"])
def health_check():
    return {"status": "online", "server_time": "active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)