from pathlib import Path
from state.project_state import get_current_project_path

class SearchFiles:
    def __init__(self):
        pass

    def read_file(self, relative_path: str, mode: str = "auto",start_line: int | None = None, end_line: int | None = None, max_chars: int = 8000) -> dict:
        
        try:
            root = get_current_project_path()
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


