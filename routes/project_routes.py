from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse, Response, HTMLResponse, FileResponse
from fastmcp import FastMCP
import state.project_state as ps
from pathlib import Path


def register_project_routes(mcp: FastMCP):

    @mcp.custom_route("/projects/all", methods=["GET"])
    async def list_projects(request: Request) -> Response:
        try:
            data = {"projects": ps.list_projects()}
            print(data)
            return JSONResponse(data)
        except Exception as e:
            print("Error occurred: ", e)
            return PlainTextResponse("Some error occurred", status_code=500)

    @mcp.custom_route("/projects/add", methods=["POST"])
    async def add_projects(request: Request) -> PlainTextResponse:
        try:
            body = await request.json()
            name, path = body.get("name"), body.get("path")
            if not name or not path:
                return PlainTextResponse("Name or path was not found", status_code=400)
            ps.add_project(name=name, path=path)
            return PlainTextResponse("Your project was recorded")
        except Exception as e:
            print("Error occured: ", e)
            return PlainTextResponse(f"Error occurred: {str(e)}", status_code=500)

    @mcp.custom_route("/projects/active", methods=["GET"])
    async def get_active_project(request: Request) -> JSONResponse:
        try:
            active_project = {
                "name": ps.get_current_project_name(),   
                "path": ps.get_current_project_path()
            }
            return JSONResponse(active_project)
        except Exception as e:
            print("Error occurred: ", str(e))
            return JSONResponse({"name": None, "path": None})  # ← safe fallback

    @mcp.custom_route("/projects/set", methods=["PUT"])
    async def set_current_project(request: Request) -> PlainTextResponse:
        try:
            body = await request.json()
            name = body.get("name")
            if not name:
                return PlainTextResponse("Name not found", status_code=400)
            ps.set_active_project(name=name)
            return PlainTextResponse("Project changed successfully.")
        except Exception as e:
            print("Error occured: ", e)
            return PlainTextResponse(f"Error occurred: {str(e)}", status_code=500)


    @mcp.custom_route("/projects/{name}", methods=["DELETE"])
    async def delete_project(request: Request) -> PlainTextResponse:
        try:
            name = request.path_params.get("name")
            if not name:
                return PlainTextResponse("Invalid request", status_code=400)
            ps.remove_project(name=name)
            return PlainTextResponse("Project deleted")
        except Exception as e:
            print("Error occured: ", e)
            return PlainTextResponse(f"Error occurred: {str(e)}", status_code=500)

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
        return FileResponse(file_path,headers={"Cache-Control":"no-store"})