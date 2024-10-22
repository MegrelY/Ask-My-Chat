# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    source_url: Optional[str] = None
