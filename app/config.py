# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    JSON_FILE_PATH: str = os.getenv('JSON_FILE_PATH') 

settings = Settings()
