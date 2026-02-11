from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This tells Python where the database file is
# Your leader's SQLite file will be named 'tempo.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./tempo.db"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# This creates a 'Session' - think of it as a phone line to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class that our data models will inherit from
Base = declarative_base()