from pathlib import Path
from tools.utils import get_current_project_path
import re

class SearchFiles:
    def __init__(self):
        with open('.gitignore', "r") as file:
            IGNORED = [line.strip() for line in file.readlines()]
        self.IGNORED = IGNORED
        pass

    def read_file(self, relative_path: str, mode: str = "auto",start_line: int | None = None, end_line: int | None = None, max_chars: int = 8000) -> dict:
        
        try:
            root = Path(get_current_project_path()).resolve()
        except Exception as e:
            return {"error":str(e)}
        
        target_file = (root / relative_path).resolve()

        if not str(target_file).startswith(str(root)):
            return {"error":"access denied"}

        if not target_file.exists():
            return {"error":"path does not exist"}
        
        if not target_file.is_file():
            return {"error":"not a file"}
        
        try:
            with open(target_file, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            return {"error":str(e)}
        
        lines = content.splitlines()
        total_lines = len(lines)

        if mode == "lines":
            if start_line is None or end_line is None:
                return {"error":"start_line and end_line is required for 'lines' mode"}
            
            start_line = max(0, start_line)
            end_line = min(total_lines - 1, end_line)

            selected = lines[start_line:end_line+1]
            final_content = "\n".join(selected)

            return {
                "path": str(target_file.relative_to(root)),
                "start_line": start_line,
                "end_line": end_line,
                "total_lines": total_lines,
                "truncated": False,
                "content": final_content
            }
        # else is used for 'auto' mode
        else:
            truncated = False
            final_content = content

            if len(content) > max_chars:
                final_content = content[:max_chars]
                truncated = True
            
            return {
                "path": str(target_file.relative_to(root)),
                "start_line": 0,
                "end_line": total_lines - 1,
                "total_lines": total_lines,
                "truncated": truncated,
                "content" : final_content
            }
        
    def grep_tool(self, query: str, is_regex: bool = False, wildcard: list[str]| None = None, scope: str = '.', max_results: int = 50) -> dict:
        
        try:
            
            root = Path(get_current_project_path()).resolve()
            search_scope = root
        except Exception as e:
            {'error': str(e)}
        
        if scope != '.':
            search_scope = (search_scope / scope).resolve()

            if not str(search_scope).startswith(root):
                return {"error": "access_denied"}
            
            if not search_scope.exists():
                return {"error": "path does not exists"}
        
        results: list[dict] = []

        for path in search_scope.iterdir():

            if path.is_file():
                pass
            