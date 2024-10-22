from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine
from .config import settings
import openai
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load OpenAI API Key
openai.api_key = settings.OPENAI_API_KEY

def call_openai_api(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ask My Chat API!"}

@app.post("/ask", response_model=schemas.AnswerResponse)
async def ask_question(request: schemas.QuestionRequest):
    # Call the function to get relevant data from the JSON file
    data, source_url = utils.get_relevant_data(request.question)

    if not data:
        return schemas.AnswerResponse(
            answer="Information not available in the provided data.",
            source_url=None
        )

    return schemas.AnswerResponse(answer=data, source_url=source_url)

logging.basicConfig(level=logging.INFO)

