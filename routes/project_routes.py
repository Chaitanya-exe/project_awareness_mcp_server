from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse, Response, HTMLResponse, FileResponse
from fastmcp import FastMCP
import state.project_state as ps
from pathlib import Path
def register_project_routes(mcp: FastMCP):

    @mcp.custom_route("/projects/all", methods=["GET"])
    async def list_projects(request: Request) -> Response:
        return JSONResponse(ps.get_state())
    
    @mcp.custom_route("/projects/add", methods=["POST"])
    async def add_projects(request: Request) -> PlainTextResponse:
        response = await request.json()
        name, path = response.get("name"), response.get("path")
        if not name or not path:
            return PlainTextResponse("Name or path was not found", status_code=400)
        ps.add_project(name=name, path=path)
        return PlainTextResponse("You response was recorded")
    
    @mcp.custom_route("/projects/{name}", methods=["DELETE"])
    async def delete_project(request: Request) -> PlainTextResponse:
        name = request.path_params.get("name")

        if not name:
            return PlainTextResponse("Invalid request", status_code=400)
        
        ps.remove_project(name=name)
        return PlainTextResponse("Project deleted")


    @mcp.custom_route("/projects/set", methods=["PUT"])
    async def set_current_project(request: Request) -> PlainTextResponse:
        response = await request.json()
        name = response.get("name")

        if not name:
            return PlainTextResponse("Name not found", status_code=404)
        
        ps.set_active_project(name=name)

        return PlainTextResponse("Project changed successfully.")
    
    @mcp.custom_route("/ui", methods=["GET"])
    async def _ui(_) -> Response:
        return HTMLResponse(Path("web/index.html").read_text())
    
    @mcp.custom_route("/static/{filename:path}", methods=["GET"])
    async def serve_static_files(request: Request) -> Response:
        WEB_DIR = Path("web").resolve()
        filename = request.path_params.get("filename")
        file_path = WEB_DIR / filename

        if not file_path.exists():
            return HTMLResponse("Not Found", status_code=404)
        
        return FileResponse(file_path)