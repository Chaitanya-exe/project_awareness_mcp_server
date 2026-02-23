from fastmcp import FastMCP
import state.project_state as ps
from pathlib import Path

class Manager():
    def __init__(self):
        pass

    def list_projects(self) -> dict:
        return ps.get_state()
    
    def add_projects(self, name: str, path: str) -> dict:

        if not name or not path:
            return {"error":"name or path not found"}
        ps.add_project(name=name, path=path)
        return {"success":"project added successfully"}

    def delete_project(self, name: str) -> dict:

        if not name:
            return {"error":"name not found"}
        
        ps.remove_project(name=name)
        return {"success":"project deleted successfully"}
    
    def set_current_project(self, name: str) -> dict:

        if not name:
            return {"error":"name was not found"}
        
        ps.set_active_project(name=name)

        return {"success":f"project '{name}' set a current project"}