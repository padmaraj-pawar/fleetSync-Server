import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This loads the variables from your .env file
load_dotenv()

# This pulls the 'DATABASE_URL' we just saved
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine using the secret URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()