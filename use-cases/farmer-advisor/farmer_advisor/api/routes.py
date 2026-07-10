"""Custom API routes for Farmer Advisor. Agent chat routes come from Agent Kernel itself."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

_WEB_DIR = Path(__file__).parents[1] / "web"

web_router = APIRouter()


@web_router.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the web chat UI."""
    return FileResponse(_WEB_DIR / "index.html")
