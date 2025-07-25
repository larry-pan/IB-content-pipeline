from pydantic import BaseModel


class GenerateMathRequest(BaseModel):
    topic: str = "Calculus"
    level: str = "SL"


class GenerateCSRequest(BaseModel):
    topic: str = "Problem-solving and Programming"
    level: str = "SL"
