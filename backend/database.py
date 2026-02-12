from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Database Connected Successfully!")
except Exception as e:
    print("Database Connection Failed:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
