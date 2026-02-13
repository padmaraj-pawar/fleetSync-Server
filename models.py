from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from database import Base
import datetime

# For Dashboard Map and individual Shipment tracking
class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    tempo_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    fuel_level = Column(Integer)
    load_weight = Column(Float) # The "Load" feature
    co2_emitted = Column(Float) # The "CO2" feature
    eta = Column(String)        # The "ETA" feature
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# For the Notification Page (Ticketing System)
class DeliveryTicket(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True) # From Team Leader
    customer_id = Column(String)
    origin = Column(String)
    destination = Column(String)
    load_type = Column(String)
    driver_id = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)