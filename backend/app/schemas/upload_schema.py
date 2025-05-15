from pydantic import BaseModel, Field, HttpUrl, model_validator
from typing import Optional, Literal
from datetime import datetime


class DocumentUploadRequest(BaseModel):
    alias: str
    summary: Optional[str] = None
    is_confidential: str  # "yes" or "no"
    password: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_password_if_confidential(cls, values):
        is_conf = values.get("is_confidential", "").lower() == "yes"
        pwd = values.get("password")

        if is_conf and (not pwd or len(pwd) < 8):
            raise ValueError("Password must be at least 8 characters when confidentiality is enabled.")
        
        return values


# ✅ Request schema when uploading a file link instead of the actual file
class DocumentLinkUploadRequest(DocumentUploadRequest):
    filelink: HttpUrl = Field(..., description="Link to the file (e.g. audio, video, or document)")

    class Config:
        schema_extra = {
            "example": {
                "alias": "demo_pitch_video",
                "summary": "Pitch video for client X",
                "is_confidential": "no",
                "filelink": "https://example.com/video.mp4"
            }
        }


# ✅ Response schema after successful document upload
class DocumentResponse(BaseModel):
    id: str
    alias: str
    summary: Optional[str] = None
    transcription: Optional[str]
    filelink: Optional[HttpUrl]
    filetype: Literal["audio", "video", "document"]
    is_confidential: Literal["yes", "no"]
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "66157b27e1c2fcf2a9cabcde",
                "alias": "demo_pitch_video",
                "summary": "Pitch video for client X",
                "transcription": "This is the transcribed content...",
                "filelink": "https://example.com/video.mp4",
                "filetype": "video",
                "is_confidential": "no",
                "created_at": "2025-04-19T18:42:01.123Z"
            }
        }
