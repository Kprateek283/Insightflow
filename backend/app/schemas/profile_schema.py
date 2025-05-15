# app/schemas/profile_schema.py
from pydantic import BaseModel
from typing import Optional

class ProfileSummary(BaseModel):
    name: str
    email: str
    total_uploads: int
    total_qna: int
    total_documents: int
    total_audio: int
    total_video: int
