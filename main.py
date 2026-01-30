from fastmcp import FastMCP
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/chaitanyayadav/personal/code/ai_projects/local_MCP_server")

mcp = FastMCP(name='local_code_access',
              instructions='This server allows the client to acces files within a specified directory and can execute git cli commands',
              )

@mcp.tool
def execute_git_command(action: str, args: list[str] | None = None, message: str | None = None) -> dict:
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



if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        print(e, file=sys.stderr)
