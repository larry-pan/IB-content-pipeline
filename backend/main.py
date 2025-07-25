from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import generator

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aa_generator = generator.AAMathGenerator()


@app.post("/generate")
def generate_question():
    question = aa_generator.generate()
    return JSONResponse(question)
