import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_CONN_URL")
        if not self.DATABASE_URL:
            raise ValueError("DB_URL environment variable not set.")

        self.engine = create_engine(self.DATABASE_URL,echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseManager()
engine = db_manager.engine
SessionLocal = db_manager.SessionLocal
Base = db_manager.Base
get_db=db_manager.get_db

