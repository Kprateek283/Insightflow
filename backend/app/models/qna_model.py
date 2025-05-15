from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QAItem(BaseModel):
    question: str
    answer: str
    timestamp: datetime = Field(default_factory=datetime.now())
    used_fallback: bool = False
    sources: Optional[List[str]] = None


class QADocument(Document):
    document_id: str
    total_qas: int = 0
    qas: List[QAItem] = []

    class Settings:
        name = "qa_pairs"
