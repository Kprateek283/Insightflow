from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserSignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    token: Optional[str] = None
    created_at: datetime
    documents: Optional[List[str]] = []
    total_qna :Optional[int] = 0
