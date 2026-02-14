from sqlalchemy import Column, Integer, String, Float, Numeric
from database import Base

class Profile(Base):
    __tablename__ = "profile"
    emailid = Column(String(255), primary_key=True)
    phoneNo = Column(Integer)
    name = Column(String(100))
    company_name = Column(String(150))
    company_address = Column(String(255))

class Shipment(Base):
    __tablename__ = "shipment"
    shipment_id = Column(Integer, primary_key=True)
    origin_lat = Column(Numeric(9,6))
    origin_long = Column(Numeric(9,6))
    destination_lat = Column(Numeric(9,6))
    destination_long = Column(Numeric(9,6))
    truck_id = Column(Integer)
    load = Column(Numeric)
    status = Column(Integer) # 1=Pending, 2=Active, 3=Delivered
    co2_emission = Column(String(10)) 
    avg_speed = Column(Float)
    distance_covered = Column(Float)

class TruckProfile(Base):
    __tablename__ = "truck_profile"
    truck_id = Column(Integer, primary_key=True)
    email_id = Column(String(255))
    phone_no = Column(String(15))
    name = Column(String(100))
    company_name = Column(String(100))
    active_status = Column(Integer)