from .config import SessionLocal, Base, engine
from . models import Project, ActiveProject

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
