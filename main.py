from fastmcp import FastMCP
import requests
import subprocess

mcp = FastMCP(name='local_code_access',
              instructions='This server allows the client to acces files within a specified directory and can execute git cli commands')

@mcp.tool
def execute_git_command(action: str, args: list[str], message: str | None) -> dict:
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
        text=True
    )
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }



if __name__ == "__main__":
    mcp.run()
