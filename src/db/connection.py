import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL_POOLED = os.getenv("DATABASE_URL_POOLED")

engine = create_engine(DATABASE_URL_POOLED)
SessionLocal = sessionmaker(bind=engine)