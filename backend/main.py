import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import generator
from models import GenerateCSRequest, GenerateMathRequest

IS_BUNDLE = getattr(sys, "frozen", False)
if IS_BUNDLE:  # PyInstaller bundle
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

STATIC_DIR = base_path / "static"
ENV_PATH = base_path / ".env"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/")
async def serve_frontend():
    index_path = STATIC_DIR / "index.html"
    return FileResponse(index_path)


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")


@app.post("/generate/math")
def generate_question(req: GenerateMathRequest):
    aa_generator = generator.MathAAGenerator(env_path=ENV_PATH)
    question = aa_generator.generate(topic=req.topic, level=req.level)
    return JSONResponse(question)


@app.post("/generate/cs")
def generate_question(req: GenerateCSRequest):
    aa_generator = generator.CSGenerator(env_path=ENV_PATH)
    question = aa_generator.generate(topic=req.topic, level=req.level)
    return JSONResponse(question)


if __name__ == "__main__":
    import uvicorn
    import webbrowser

    print("Loading demo...")
    print("Demo is now live on http://localhost:8000/")
    webbrowser.open("http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
