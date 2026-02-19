from fastmcp import FastMCP
from tools import register_git_tools, register_project_structure_tools
from routes.project_routes import register_project_routes
import sys

mcp = FastMCP(name='local_code_access',
              instructions='This server allows the client to acces files within a specified directory and can execute git cli commands and basic shell commands',
            )

register_git_tools(mcp)
register_project_structure_tools(mcp)
register_project_routes(mcp)


if __name__ == "__main__":
    try:
        mcp.run(transport="http")
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        print(e, file=sys.stderr)
