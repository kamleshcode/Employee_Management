import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_CONN_URL")
if not db_url:
    print("Error: DATABASE_URL not found in .env file!")
pool_size = int(os.getenv("DB_POOL_SIZE", 5))
max_overflow = int(os.getenv("DB_MAX_OVERFLOW", 10))

engine = None
Session = None

try:
    engine = create_engine(db_url,
                           pool_size=pool_size,
                           max_overflow=max_overflow,
                           pool_timeout=30,
                           echo=True)
    Session = sessionmaker(bind=engine)
    print("Database engine initialized successfully.....")
except Exception as e:
    print(f"Error initializing the database engine: {e}")

Base = declarative_base()

# Employee Model
class Employee(Base):
    __tablename__ = 'Employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    department = Column(String(50))
    salary = Column(Float)
    phoneNumber = Column(String(20))
    isActive = Column(Boolean)

Base.metadata.create_all(engine)





