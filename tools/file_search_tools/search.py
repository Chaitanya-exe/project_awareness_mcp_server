from pathlib import Path
from ..utils import get_current_project_path
import re
from fnmatch import fnmatch
import os

class SearchFiles:
    def __init__(self):
        self.IGNORED_DIRS = {
            ".git",
            ".venv",
            "node_modules",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache"
        }

    def _load_ignored(self):
        
        root = Path(get_current_project_path()).resolve()

        gitignore = (root / '.gitignore').resolve()
        ignored = set(self.IGNORED_DIRS)
        if gitignore.exists():

            with open(gitignore, "r") as f:

                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue
                    ignored.add(line.rstrip("/"))
        
        return ignored


    def _is_ignored(self, name: str, patterns: set[str]) -> bool:
        return any(fnmatch(name, pattern) for pattern in patterns)
    
    def _is_binary(self, file: Path):
        try:
            with open(file, "rb") as f:
                chunk = f.read(8192)
            return b"\x00" in chunk
        except Exception as e:
            return True


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
            return {'error': str(e)}
        
        if scope != '.':
            search_scope = (search_scope / scope).resolve()

            if not str(search_scope).startswith(str(root)):
                return {"error": "access_denied"}
            
            if not search_scope.exists():
                return {"error": "path does not exists"}
        
        results: list[dict] = []
        
        flags = re.IGNORECASE
        pattern_str = query if is_regex else re.escape(query)
        
        try:
            pattern = re.compile(pattern_str, flags)
        except re.error as e:
            return {"error": str(e)}

        globs = wildcard if wildcard else ["*"]
        ignored = self._load_ignored()

        for dirpath, dirnames, filenames in os.walk(search_scope):
            dirnames[:] = [d for d in dirnames if not self._is_ignored(d, ignored)]

            filenames[:] = [f for f in filenames if self._is_ignored(f, globs)]

            for file in filenames:
                file_path = Path(dirpath) / file
                if self._is_binary(file_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.read().splitlines()
                except Exception as e:
                    continue

                for idx, line in enumerate(lines):
                    
                    if pattern.search(line):
                        start = max(0, idx - 5)
                        end = min(len(lines), idx + 5 + 1)

                        context_before = lines[start:idx]
                        context_after = lines[idx+1 :end]

                        results.append({
                            "file": str(file_path.relative_to(root)),
                            "line": idx+1,
                            "match": line,
                            "context_before": context_before,
                            "context_after": context_after
                        })

                        if len(results) >= max_results:
                            return {
                                "query": query,
                                "total_matches": len(results),
                                "capped": True,
                                "results": results
                            }
        
        return {
            "query": query,
            "capped": False,
            "total_matches": len(results),
            "results": results
        }