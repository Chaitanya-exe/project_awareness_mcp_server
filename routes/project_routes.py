from starlette.requests import Request
from starlette.responses import PlainTextResponse
from fastmcp import FastMCP
def register_project_routes(mcp: FastMCP):

    @mcp.custom_route("/projects", methods=["GET"])
    async def list_projects(request: Request) -> PlainTextResponse:
        return PlainTextResponse("You can see projects here")