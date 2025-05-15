# app/models/document_model.py

from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional, Literal
from datetime import datetime

class DocumentModel(Document):
    user_id: PydanticObjectId  # Retrieved using get_current_user

    alias: str = Field(..., description="Unique name or identifier for the document")
    summary: Optional[str] = Field(None, description="Optional summary of the document")
    transcription: Optional[str] = Field(None, description="Transcript if audio/video")

    created_at: datetime = Field(default_factory=datetime.now)

    filelink: Optional[str] = Field(None, description="Link to file (only for link uploads)")
    filetype: Literal["audio", "video", "document"] = Field(..., description="Type of the uploaded file")

    is_confidential: Literal["yes", "no"] = Field(..., description="Whether document is confidential")
    hashed_password: Optional[str] = Field(
        None, description="Required only when document is confidential"
    )

    class Settings:
        name = "documents"

    class Config:
        schema_extra = {
            "example": {
                "user_id": "660d13e90dcf4455e7c1234f",
                "alias": "project_notes_march",
                "summary": "Summary of meeting notes",
                "transcription": "Text of the transcript",
                "filelink": "https://some-link.com/file.pdf",
                "filetype": "document",
                "is_confidential": "yes",
                "hashed_password": "$2b$12$examplehashstring...",
            }
        }
