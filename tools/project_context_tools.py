from fastmcp.tools import tool
import subprocess
from pydantic import BaseModel, Field
from state.project_state import get_current_project_path

class GitParameters(BaseModel):
    action: str = Field(..., description="The git action to perform (status, diff, log, branch, add, commit)")
    args: list[str] | None = Field(default=None, description="Optional arguments for the git command")
    message: str | None = Field(default=None, description="Commit message (required for 'commit' action)")

class Git:
    def __init__(self):
        pass

    def _run_git(self, args: list[str]) -> subprocess.CompletedProcess:
        root = get_current_project_path()

        return subprocess.run(
            ["git"] + args,
            cwd=root,
            capture_output=True,
            text=True
        )
    

    @tool()
    def get_git_status_structured(self) -> dict:

        result = self._run_git(["status","--porcelain", "-b"])

        if result.returncode != 0:
            return {
                "error" : result.stderr
            }
        
        lines: list[str] = result.stdout.strip().splitlines()

        branch = None
        modified = []
        staged = []
        untracked = []

        for line in lines:
            if line.startswith("##"):
                branch = line.replace("##","").strip()
                continue