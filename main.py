from fastmcp import FastMCP
from tools.git_executor import Git
from routes.project_routes import register_project_routes
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/chaitanyayadav/personal/code/ai_projects/local_MCP_server")

mcp = FastMCP(name='local_code_access',
              instructions='This server allows the client to acces files within a specified directory and can execute git cli commands',
              )

mcp.add_tool(Git().execute_git_command)
register_project_routes(mcp)



if __name__ == "__main__":
    try:
        mcp.run(transport="http")
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        print(e, file=sys.stderr)
