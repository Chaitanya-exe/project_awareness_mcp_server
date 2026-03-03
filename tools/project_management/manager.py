from fastmcp import FastMCP
import state.project_state as ps
from pathlib import Path
from db.config import SessionLocal
from db.models import Projects, ActiveProject

class Manager:
    def __init__(self):
        self.session = SessionLocal

    def list_projects(self) -> dict:
        with self.session() as session:
            projects = session.query(Projects).all()
            return { p.name :p.path for p in projects}
    
    def add_projects(self, name: str, path: str) -> dict:
        with self.session() as session:
            existing = session.get(Projects, name)
            if existing:
                raise ValueError(f"Project with name: {name} already exists")
            project = Projects(name=name, path=path)
            session.add(project)
            session.commit()
            return {"success":f"project {name} created successfully"}

    def delete_project(self, name: str) -> dict:
        with self.session() as session:
            exists = session.get(Projects, name)
            if not exists:
                raise ValueError(f"Project with name: {name} does not exists")
            
            session.delete(exists)
            session.commit()
            return {"success":f"project {name} deleted successfully"}
    
    def set_current_project(self, name: str) -> dict:
        with self.session() as session:
            project = session.get(Projects, name)
            if not project:
                raise ValueError(f"project with {name} does not exists")
            
            active = session.query(ActiveProject).first()
            if not active:
                active = ActiveProject(project_name=name)
                session.add(active)
            else:
                active.project_name = name
            
            session.commit()
            return {"success":f"{name} is the current active project"}