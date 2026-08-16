from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

metadata = MetaData()
try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print("Database connection failed:", e)