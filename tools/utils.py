from db.config import SessionLocal
from db.models import ActiveProject
def get_current_project_path() -> str:
    with SessionLocal() as session:
        active_project = session.query(ActiveProject).first()

        if not active_project:
            raise ValueError(f"No project activated yet...")
        
        return str(active_project.project.path)
