from sqlalchemy import Column, Integer, String, Float, Numeric
from database import Base

class Profile(Base):
    __tablename__ = "profile"
    emailid = Column(String(255), primary_key=True)
    phoneNo = Column(Integer) # PDF says int(15) [cite: 5, 71, 141, 207]
    name = Column(String(100), nullable=False) # NN [cite: 7, 73, 143, 209]
    company_name = Column(String(150))
    company_address = Column(String(255))

class Shipment(Base):
    __tablename__ = "shipment"
    shipment_id = Column(Integer, primary_key=True)
    # Coordinates must be Numeric(9,6) NN [cite: 47-53, 116-122, 183-189, 252-258]
    origin_lat = Column(Numeric(9,6), nullable=False)
    origin_long = Column(Numeric(9,6), nullable=False)
    destination_lat = Column(Numeric(9,6), nullable=False)
    destination_long = Column(Numeric(9,6), nullable=False)
    truck_id = Column(Integer, nullable=False) # NN [cite: 55, 125, 191, 261]
    load = Column(Numeric, nullable=False) # NN [cite: 57, 127, 193, 263]
    status = Column(Integer, nullable=False) # NN [cite: 59, 129, 195, 265]
    co2_emission = Column(String(10), nullable=False) # NN + Typo match [cite: 131, 267]
    avg_speed = Column(Float)
    distance_covered = Column(Float, nullable=False) # NN [cite: 65, 135, 201, 271]

class TruckProfile(Base):
    __tablename__ = "truck_profile"
    truck_id = Column(Integer, primary_key=True)
    email_id = Column(String(255), nullable=False) # NN [cite: 32, 100, 168, 236]
    phone_no = Column(String(15))
    name = Column(String(100), nullable=False) # NN [cite: 36, 105, 172, 241]
    company_name = Column(String(100))
    active_status = Column(Integer, nullable=False) # NN [cite: 42, 111, 178, 247]