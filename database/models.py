from sqlalchemy import Column, Integer, String
from .database import Base  # Correct import path

class CodeInteraction(Base):
    __tablename__ = "code_interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Add autoincrement=True
    prompt = Column(String, index=True)
    language = Column(String, index=True)
    generated_code = Column(String)
    reasoning = Column(String)
    session_id = Column(String, index=True)