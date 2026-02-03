from fastmcp.tools import tool
import subprocess
from pydantic import BaseModel, Field

class GitParameters(BaseModel):
    action: str = Field(..., description="The git action to perform (status, diff, log, branch, add, commit)")
    args: list[str] | None = Field(default=None, description="Optional arguments for the git command")
    message: str | None = Field(default=None, description="Commit message (required for 'commit' action)")

class Git:
    def __init__(self):
        pass
    
    @tool()
    def execute_git_command(self, action: str, args: list[str] | None = None, message: str | None = None) -> dict:
        """
        This tool allows the client to execute git CLI commands
        the current actions allowed are:
        status,
        diff,
        log,
        branch,
        add
        commit,
        """
        allowed_actions = [
            "status",
            "diff",
            "log",
            "branch",
            "add",
            "commit"]
        
        if action not in allowed_actions:
            return {
                "stdout":"",
                "stderr":'This action is not allowed',
                "returncode":1
            }
        command = ['git', action]
        if action == "commit":
            if not message:
                return {
                    "stdout":"",
                    "stderr":'a commit message is required',
                    "returncode":1
                }
            
            command.extend(['-m', message])
            
        if args:
            command.extend(args)


        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            cwd=REPO_ROOT
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }