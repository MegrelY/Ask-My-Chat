# app/models.py
from sqlalchemy import Column, Integer, JSON
from .database import Base

class DataItem(Base):
    __tablename__ = 'web_data2'

    id = Column(Integer, primary_key=True, index=True)
    json_data = Column(JSON, nullable=True)  # Use json_data to store JSON data
