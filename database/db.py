from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


Base = declarative_base()
env = os.getenv("ENV","development")
path = f'.env.{env}'
dotenv_path = os.path.join('environments', path)
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_CONECTION_STRING")
engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()