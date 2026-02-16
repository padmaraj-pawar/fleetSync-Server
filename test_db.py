# ...existing code...
from dotenv import load_dotenv
import os, sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()  # loads .env into environment

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("ERROR: DATABASE_URL not found in environment (check .env).")
    sys.exit(1)

try:
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        row = result.fetchone()
    if row and row[0] == 1:
        print("Success: connected to database and SELECT 1 returned 1")
    else:
        print("Connected but unexpected result from SELECT 1:", row)
except SQLAlchemyError as e:
    print("SQLAlchemyError:", str(e))
except Exception as e:
    print("Error:", str(e))