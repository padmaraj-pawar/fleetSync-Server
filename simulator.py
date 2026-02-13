import requests
import time
import random

API_URL = "http://127.0.0.1:8000/telemetry/ingest"

trucks = ["Tempo-01", "Tempo-02", "Tempo-03"]

print("Starting Simulation... Press Ctrl+C to stop.")

while True:
    for truck in trucks:
        payload = {
            "tempo_id": truck,
            "lat": 18.5 + random.uniform(-0.1, 0.1),
            "lon": 73.8 + random.uniform(-0.1, 0.1),
            "temp": random.uniform(2.0, 8.0),
            "co2": random.uniform(1.0, 5.0)
        }
        try:
            response = requests.post(API_URL, json=payload)
            print(f"Sent data for {truck}: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    
    time.sleep(10) # Send updates every 10 seconds