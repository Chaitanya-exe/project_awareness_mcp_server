from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

URL = os.getenv("DATABASE_URL","postgresql+psycopg://mcp_user:mcp_pass1234@localhost:5432/mcp_server")


engine = create_engine(URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass