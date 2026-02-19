from .git_tools.git import Git
from .project_tree_tool.tree import ProjectStructure
from fastmcp import FastMCP

git_tool = Git()
structure_tool = ProjectStructure()

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