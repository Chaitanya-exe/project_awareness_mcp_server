from pathlib import Path
from state.project_state import get_current_project_path

IGNORED_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache"
}

class ProjectStructure:
    def __init__(self):
        pass

    def _build_tree(self, path: Path, max_depth: int, curr_depth: int):
        if curr_depth >= max_depth:
            return []
        
        nodes = []

        for item in sorted(path.iterdir()):
            if item.name in IGNORED_DIRS:
                continue

            if item.is_dir():
                nodes.append({
                    "type":"directory",
                    "name": item.name,
                    "children": self._build_tree(item, max_depth, curr_depth+1)
                })
            else:
                nodes.append({
                    "type":"file",
                    "name":item.name
                })
        
        return nodes
    
    def get_project_tree(self, depth: int = 2) -> dict:
        try:
            root = get_current_project_path()
        except Exception as e:
            return {"error":str(e)}
        
        tree = self._build_tree(root, depth, 0)

        return {
            "root" : root.name,
            "depth": depth,
            "tree": tree
        }
    
    def list_directory(self, relative_path: str = '.') -> dict:
        
        try:
            root = get_current_project_path()
        except Exception as e:
            return {"error": str(e)}
        
        target_path = (root / relative_path).resolve()

        if not str(target_path).startswith(str(root)):
            return {"error":"access denied"}
        
        if not target_path.exists():
            return {"error":"path does not exist"}

        if not target_path.is_dir():
            return {"error":"not a directory"}

        files = []
        directories = []

        for item in target_path.iterdir():

            if item.name in IGNORED_DIRS:
                continue

            if item.is_dir():
                directories.append(item.name)
            else:
                files.append(item.name)

        return {
            "path": str(target_path.relative_to(root)),
            "directories": directories,
            "files": files
        }

