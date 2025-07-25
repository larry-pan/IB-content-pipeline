import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

app = FastAPI()

# Path to static directory (e.g., React or Vue build)
STATIC_DIR = Path(__file__).parent / "static"

# Mount the static directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Fallback for SPA routing (serves index.html)
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"error": "index.html not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)