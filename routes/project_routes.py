from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse, Response, HTMLResponse
from fastmcp import FastMCP
import state.project_state as ps
from pathlib import Path
def register_project_routes(mcp: FastMCP):

    @mcp.custom_route("/projects/all", methods=["GET"])
    async def list_projects(request: Request) -> Response:
        return JSONResponse(ps.get_state())
    
    @mcp.custom_route("/projects/add", methods=["POST"])
    async def add_projects(request: Request) -> PlainTextResponse:
        return PlainTextResponse("You can see projects here")
    
    @mcp.custom_route("/projects/delete", methods=["DELETE"])
    async def delete_project(request: Request) -> PlainTextResponse:
        return PlainTextResponse("You can see projects here")
    
    @mcp.custom_route("/projects/set", methods=["PUT"])
    async def set_current_project(request: Request) -> PlainTextResponse:
        return PlainTextResponse("You can see projects here")
    
    @mcp.custom_route("/ui", methods=["GET"])
    async def _ui(_) -> Response:
        return HTMLResponse(Path("web/index.html").read_text())