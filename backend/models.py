from pydantic import BaseModel


class GenerateRequest(BaseModel):
    topic: str = "Calculus"
    max_iterations: int = 3
    acceptable_score: int = 95
