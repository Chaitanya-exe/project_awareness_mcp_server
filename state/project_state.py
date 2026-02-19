import json
from pathlib import Path
from threading import Lock

DATA_FILE = Path("data/projects.json")
LOCK = Lock()

def _load():
    if not DATA_FILE.exists():
        return {
            "active_project": None,
            "projects": {}
        }
    
    return json.loads(DATA_FILE.read_text())

def _save(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=4))

def get_state():
    with LOCK:
        return _load()
    
def add_project(name: str, path: str):
    with LOCK:
        data = _load()
        if name in data["projects"]:
            raise ValueError(f"project with {name} already exists")
        
        data["projects"][name] = path
        _save(data)

def remove_project(name: str):
    with LOCK:
        data = _load()
        data["projects"].pop(name, None)
        if data["active_project"] == name:
            data["active_project"] = None
        _save(data)

def set_active_project(name: str):
    with LOCK:
        data = _load()
        if name not in data["projects"]:
            raise ValueError(f"project with {name} does not exists")
        data["active_project"] = name
        _save(data)

def get_current_project_path() -> Path:
    data = _load()
    name = data["active_project"]

    if not name:
        raise RuntimeError("No active project set.")

    return Path(data["projects"][name]).resolve()

