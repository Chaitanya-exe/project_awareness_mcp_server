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
    


    def get_git_status_structured(self) -> dict:
        """
        
        """

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

            status_code = line[:2]
            file_path = line[3:]

            if status_code == "??":
                untracked.append(file_path)
            elif status_code[0] != " ":
                staged.append(file_path)
            elif status_code[1] != " ":
                modified.append(file_path)
        
        return {
            "branch": branch,
            "modified" : modified,
            "staged" : staged,
            "untracked": untracked
        }
    


    def get_recent_commits(self, limit: int = 10) -> dict:
        result = self._run_git([
            "log",
            f"-n{limit}",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=iso"
        ])

        if result.returncode != 0:
            return {"error": result.stderr}
        
        commits = []
        lines: list[str] = result.stdout.splitlines()
        for line in lines:
            parts = line.split("|", 3)

            if len(parts) == 4:
                commits.append({
                    "hash" : parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "message": parts[3]
                })
        
        return { "commits": commits}
    

    def get_branches(self) -> dict:
        result = self._run_git(["branch", "--format=%(refname:short)"])

        if result.returncode != 0:
            return {"error": result.stderr}

        branches = result.stdout.strip().splitlines()

        return {"branches": branches}
    

    def get_branches(self) -> dict:
        result = self._run_git(["branch", "--format=%(refname:short)"])

        if result.returncode != 0:
            return {"error": result.stderr}

        branches = result.stdout.strip().splitlines()

        return {"branches": branches}
    
    def get_diff(self, file: str | None = None) -> dict:
        args = ["diff"]
        if file:
            args.append(file)

        result = self._run_git(args)

        if result.returncode != 0:
            return {"error": result.stderr}

        return {"diff": result.stdout}


    def get_repo_info(self) -> dict:
        result = self._run_git(["rev-parse", "--show-toplevel"])

        if result.returncode != 0:
            return {"error": result.stderr}

        return {"repo_root": result.stdout.strip()}