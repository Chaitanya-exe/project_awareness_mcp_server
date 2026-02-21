from .git_tools.git import Git
from .project_tree_tool.tree import ProjectStructure
from .file_search_tools.search import SearchFiles
from fastmcp import FastMCP

git_tool = Git()
structure_tool = ProjectStructure()
file_tool = SearchFiles()

def register_git_tools(mcp: FastMCP):

    @mcp.tool
    def get_git_status() -> dict:
        """
    Retrieve the current Git repository status in structured form.

    This tool inspects the active project repository and returns:
    - The current branch name
    - Files staged for commit
    - Modified (unstaged) files
    - Untracked files

    Returns:
        dict:
            {
                "branch": str | None,
                "staged": list[str],
                "modified": list[str],
                "untracked": list[str]
            }

    Notes:
        - Uses `git status --porcelain -b` for machine-readable parsing.
        - If no active project is set, or the directory is not a git repository,
          an error dictionary will be returned.

    Failure Response:
        {
            "error": str
        }
    """
        return git_tool.get_git_status_structured()
    
    @mcp.tool
    def get_recent_commits(limit: int = 10) -> dict:
        """
    Retrieve recent commit history from the active project repository.

    Args:
        limit (int, optional):
            The maximum number of recent commits to return.
            Defaults to 10.

    Returns:
        dict:
            {
                "commits": [
                    {
                        "hash": str,
                        "author": str,
                        "date": str,
                        "message": str
                    },
                    ...
                ]
            }

    Notes:
        - Commits are returned in reverse chronological order (most recent first).
        - Uses a machine-readable git log format for structured parsing.

    Failure Response:
        {
            "error": str
        }
    """
        return git_tool.get_recent_commits(limit)
    
    @mcp.tool
    def get_branches() -> dict:
        """
    List all local branches in the active project repository.

    Returns:
        dict:
            {
                "branches": list[str]
            }

    Notes:
        - Only local branches are returned.
        - The current active branch can be determined via `get_git_status()`.

    Failure Response:
        {
            "error": str
        }
    """
        return git_tool.get_branches()
    
    @mcp.tool
    def get_diff(file: str | None = None) -> dict:
        """
    Retrieve the current working directory diff from the active project repository.

    Args:
        file (str | None, optional):
            If provided, returns the diff for a specific file relative to the
            working directory. If None, returns the full repository diff.

    Returns:
        dict:
            {
                "diff": str
            }

    Notes:
        - Shows unstaged changes by default.
        - To inspect staged changes, this tool may be extended in the future.
        - Useful for reviewing modifications before committing.

    Failure Response:
        {
            "error": str
        }
    """
        return git_tool.get_diff(file)
    

def register_project_structure_tools(mcp: FastMCP):

    @mcp.tool
    def get_project_structure(depth: int = 2) -> dict:  
        """
    Retrieve a structured directory tree of the active project.

    This tool provides a hierarchical view of the project's filesystem
    up to a specified depth. It is intended to give high-level structural
    awareness of the repository without reading file contents.

    Args:
        depth (int, optional):
            Maximum directory traversal depth.
            Depth is measured relative to the project root.
            Default is 2.

    Returns:
        dict:
            {
                "root": str,         # Name of the project root directory
                "depth": int,        # Depth used for traversal
                "tree": [
                    {
                        "type": "directory" | "file",
                        "name": str,
                        "children": list | None  # Present only for directories
                    },
                    ...
                ]
            }

    Behavior:
        - Traverses the filesystem starting from the active project root.
        - Skips common large or irrelevant directories such as:
            .git, .venv, node_modules, __pycache__, etc.
        - Does not read file contents.
        - Does not follow symlinks outside the project root.
        - Traversal is strictly bounded by the `depth` parameter.

    Intended Use:
        - Understand project architecture.
        - Identify key folders and modules.
        - Decide which files to inspect next.
        - Combine with `search_files` or `read_file` for deeper analysis.

    Failure Response:
        {
            "error": str
        }
    """
        return structure_tool.get_project_tree(depth)
    
    @mcp.tool
    def list_directory(relative_path: str = ".") -> dict:
        """
    List files and subdirectories within a specified project-relative directory.

    This tool provides a non-recursive view of the contents of a directory
    inside the active project. It is intended for targeted exploration after
    identifying a relevant folder using `get_project_tree`.

    Args:
        relative_path (str, optional):
            Path relative to the active project root.
            Defaults to "." (project root).

    Returns:
        dict:
            {
                "path": str,           # The resolved project-relative directory
                "directories": list[str],
                "files": list[str]
            }

    Behavior:
        - Only lists immediate children (non-recursive).
        - Traversal is restricted to the active project root.
        - Prevents directory traversal outside the project.
        - Skips common large or irrelevant directories such as:
            .git, .venv, node_modules, __pycache__, etc.
        - Does not read file contents.

    Intended Use:
        - Explore a specific folder in detail.
        - Identify candidate files to inspect next.
        - Narrow context before calling `read_file`.

    Failure Response:
        {
            "error": str
        }
    """
        return structure_tool.list_directory(relative_path)
    

def register_file_tools(mcp: FastMCP):

    @mcp.tool
    def read_files(relative_path: str, mode: str = "auto",start_line: int | None = None, end_line: int | None = None, max_chars: int = 8000):
        """
    Read the contents of a file within the active project in a controlled manner.

    This tool retrieves file content relative to the active project root.
    It supports full-file reading with automatic truncation, or selective
    line-based reading for precise inspection.

    Args:
        relative_path (str):
            Path to the file relative to the active project root.

        mode (str, optional):
            Reading mode. Supported values:
                - "auto": Return full file content, truncated to `max_chars`
                          if necessary.
                - "lines": Return only the specified line range.
            Default is "auto".

        start_line (int | None, optional):
            Required when mode="lines".
            Starting line number (0-indexed).

        end_line (int | None, optional):
            Required when mode="lines".
            Ending line number (0-indexed, inclusive).

        max_chars (int, optional):
            Maximum number of characters returned in "auto" mode.
            Default is 8000.

    Returns:
        dict:
            {
                "path": str,          # Project-relative file path
                "start_line": int,    # First line returned
                "end_line": int,      # Last line returned
                "total_lines": int,   # Total lines in file
                "truncated": bool,    # Whether content was truncated
                "content": str        # File content (or selected portion)
            }

    Behavior:
        - Access is restricted to files within the active project root.
        - Directory traversal outside the project is blocked.
        - Only read access is performed (no modification).
        - In "auto" mode, content exceeding `max_chars` is truncated.
        - In "lines" mode, only the specified line range is returned.

    Intended Use:
        - Inspect specific modules or scripts.
        - Review implementation details before refactoring.
        - Combine with `search_files` to read relevant sections.
        - Expand context gradually to avoid excessive token usage.

    Failure Response:
        {
            "error": str
        }
    """
        return file_tool.read_file(relative_path, mode, start_line, end_line, max_chars)
