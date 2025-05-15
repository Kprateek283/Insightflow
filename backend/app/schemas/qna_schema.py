from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QAItemSchema(BaseModel):
    question: str
    answer: Optional[str] = None
    timestamp: datetime
    used_fallback: bool
    sources: Optional[List[str]] = None

    class Config:
        orm_mode = True

class QADocumentSchema(BaseModel):
    document_id: str
    total_qas: int
    qas: List[QAItemSchema]

    class Config:
        orm_mode = True
