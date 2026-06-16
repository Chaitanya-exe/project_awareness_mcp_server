import json
from pathlib import Path
from threading import Lock
from contextlib import contextmanager
from db.config import SessionLocal
from db.models import Project, ActiveProject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session


DATA_FILE = Path("data/projects.json").resolve()
LOCK = Lock()

@contextmanager
def _session():
    """
    get a db session for the local database to handle rollback/commit automatically
    """

    db_session = SessionLocal()

    try:
        yield db_session
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()
    
def _ensure_active_row(db: Session) -> ActiveProject:
    row = db.get(ActiveProject, 1)
    
    if row is None:
        row = ActiveProject(id=1, project_name=None)
        db.add(row)
        db.flush()
    
    return row
    
def add_project(name: str, path: str):
    
    with _session() as db:
        existing = db.get(Project, name)

        if existing:
            raise RuntimeError(f"Project with {name} already exists.")

        project = Project(name=name, path=path)
        db.add(project)
        return { "success": True, "project": {"name": name, "path": path}}
    

def remove_project(name: str):
    
    with _session() as db:
        existing = db.get(Project, name)

        if existing is None:
            raise RuntimeError("Project '{name}' doesn't exist.")

        db.delete(existing)
        return {"success": True, "removed":name} 


def list_projects() -> list[dict]:

    with _session() as db:

        projects = db.query(Project).order_by(Project.name).all()

        return [p.to_dict() for p in projects]

def set_active_project(name: str):
    
    with _session() as db:
        project = db.get(Project, name)

        if not project:
            raise RuntimeError(f"Project '{name}' does not exist.")
        
        row = _ensure_active_row(db)
        row.project_name = name

        return {"success": True, "active_project":name}

def get_current_project_path() -> str:
    
    with _session() as db:

        row = db.get(ActiveProject, 1)

        if row is None or row.project_name is None:
            raise RuntimeError("No active project set. Set an active project first.")

        project = db.get(Project, row.project_name)

        if not project:
            raise RuntimeError(f"Project '{row.project_name}' no longer exists.")

        return project.path    

def get_current_project_name() -> str:

    with _session() as db:

        row = db.get(ActiveProject, 1)

        if row is None:
            raise RuntimeError("No active project set. Set an active project first.")
        
        return row.project_name
    