from fastmcp import FastMCP
from tools import register_git_tools, register_project_structure_tools, register_file_tools
from routes.project_routes import register_project_routes
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Run the MCP server with optional configurations"
    )

    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode for the MCP server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="configure the port for MCP server"
    )


    mcp = FastMCP(name='project_context_interface',
                instructions='This mcp server allows the MCP clients to execute various tools to get information about a project in a specified directory, clients can access repo information, project structure and read files for full project context.',
                )

    register_git_tools(mcp)
    register_project_structure_tools(mcp)
    register_file_tools(mcp)
    register_project_routes(mcp)

    args = parser.parse_args()

    if args.mode.startswith("http"):
        mcp.run(transport="http")
    else:
        mcp.run()



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        print(e, file=sys.stderr)
