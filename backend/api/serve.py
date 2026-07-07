"""MCS Parakh — single-container entrypoint (T-301).

Mounts the API under /api (the frontend's default base, see frontend/src/api.js)
and serves the built React app from the same process, so one image is the whole
demo: `docker compose up` then open http://localhost:8000. Interactive OpenAPI
docs live at /api/docs. Bare `uvicorn api.main:app` remains the API-only dev
path; this wrapper adds nothing to the scoring path.
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from api.main import app as api_app

STATIC_DIR = Path(
    os.environ.get("PARAKH_STATIC", Path(__file__).resolve().parents[2] / "frontend" / "dist")
)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/api", api_app)


@app.get("/{full_path:path}", include_in_schema=False)
async def spa(full_path: str):
    """Static files with SPA fallback: unknown paths get index.html so
    react-router deep links (e.g. /card/<gstin>) survive a hard refresh."""
    if not STATIC_DIR.is_dir():
        return JSONResponse(
            {"detail": "Frontend build not found — the API is mounted under /api."},
            status_code=404,
        )
    root = STATIC_DIR.resolve()
    candidate = (root / full_path).resolve()
    if full_path and candidate.is_file() and candidate.is_relative_to(root):
        return FileResponse(candidate)
    return FileResponse(root / "index.html")
