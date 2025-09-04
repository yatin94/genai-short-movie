from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_host = os.getenv("DB_HOST")
database_port = os.getenv("DB_PORT", "5432")
database_name = os.getenv("DB_NAME")


DATABASE_URL = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()