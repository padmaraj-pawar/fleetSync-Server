from sqlalchemy import Column, Integer, String, Float
from database import Base

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    tempo_id = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    carbon_emitted = Column(Float) # Calculated by Pathway