import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import generator
from models import GenerateCSRequest, GenerateMathRequest

IS_BUNDLE = getattr(sys, "frozen", False)


def get_static_path():
    if IS_BUNDLE:  # PyInstaller bundle
        return Path(sys._MEIPASS) / "static"
    return Path(__file__).parent / "static"


STATIC_DIR = get_static_path()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


@app.post("/generate/math")
def generate_question(req: GenerateMathRequest):
    aa_generator = generator.MathAAGenerator()
    question = aa_generator.generate(topic=req.topic, level=req.level)
    return JSONResponse(question)


@app.post("/generate/cs")
def generate_question(req: GenerateCSRequest):
    aa_generator = generator.CSGenerator()
    question = aa_generator.generate(topic=req.topic, level=req.level)
    return JSONResponse(question)


if __name__ == "__main__":
    import uvicorn
    import webbrowser

    print("Loading demo...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
    print("Demo is now live on http://localhost:8000/")
    webbrowser.open("http://localhost:8000")
