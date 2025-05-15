from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    id: Optional[str] = None
    alias: str
    summary: Optional[str]
    transcription: Optional[str] 
    filelink: Optional[str]
    filetype: str
    is_confidential: str
    created_at: datetime
    total_qas:Optional[int]=0


class UnlockDocumentRequest(BaseModel):
    password: str

class UnlockDocumentResponse(BaseModel):
    summary : str
    transcription : str