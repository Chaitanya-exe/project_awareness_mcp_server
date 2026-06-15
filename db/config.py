from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

_DB_PATH = os.getenv("DB_PATH")
URL = f"sqlite:///{_DB_PATH}"


engine = create_engine(URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()