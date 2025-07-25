from fastapi import FastAPI
import generator

app = FastAPI()

aa_generator = generator.AAMathGenerator()


@app.post("/generate")
def generate_question():
    
    return {"question": aa_generator.generate()}
