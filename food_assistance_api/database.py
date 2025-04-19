from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base   # apparently deprecated
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
session = SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)