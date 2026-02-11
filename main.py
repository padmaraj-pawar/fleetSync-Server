from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
import uvicorn
import models 
import database
import asyncio # Moved this to the top imports for cleanliness

# 1. ALWAYS initialize the App first
app = FastAPI(title="Tempo Delivery System")

# 2. Initialize the database
models.Base.metadata.create_all(bind=database.engine)

# 3. Database Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CATEGORY A: ADMIN DOMAIN ---

@app.get("/admin/fleet/live")
def get_fleet_status(db: Session = Depends(get_db)):
    all_data = db.query(models.Telemetry).all()
    return {"live_fleet_data": all_data}

@app.get("/admin/alerts/priority")
def get_priority_alerts():
    return {"alerts": ["Tempo T-05: Milk expiring in 15 mins"]}

@app.get("/admin/analytics/emissions")
def get_emissions():
    return {"transport_co2": "45kg", "refrigeration_co2": "12kg"}

# --- CATEGORY B: USER/SHOP DOMAIN ---

@app.get("/shop/delivery/{order_id}")
def get_order_status(order_id: str):
    return {"order_id": order_id, "status": "Shipped", "ETA": "14:30"}

# --- CATEGORY C: SYSTEM/PATHWAY DOMAIN ---

@app.post("/telemetry/ingest")
def ingest_telemetry(data: dict, db: Session = Depends(get_db)):
    new_entry = models.Telemetry(
        tempo_id=data.get("tempo_id"),
        latitude=data.get("lat"),
        longitude=data.get("lon"),
        temperature=data.get("temp"),
        carbon_emitted=0.0 
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"status": "Successfully Saved", "database_id": new_entry.id}

@app.post("/pathway/webhook")
def pathway_notification(payload: dict):
    return {"msg": "Alert received from Pathway logic"}

# THIS IS THE ONE WE ARE LOOKING FOR
@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {"event": "Tempo Movement", "lat": 12.34, "lon": 56.78}
            await websocket.send_json(data)
            await asyncio.sleep(2) 
    except Exception as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)