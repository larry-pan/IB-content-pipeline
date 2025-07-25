from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import generator
from models import GenerateRequest

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
def generate_question(req: GenerateRequest):
    print(req.topic)
    question = aa_generator.generate(topic=req.topic)
    return JSONResponse(question)
