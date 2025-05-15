from beanie import Document, PydanticObjectId
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime

class User(Document):
    name: str
    email: EmailStr
    password: str
    created_at: datetime
    documents : List[PydanticObjectId] = []  # List of document IDs associated with the user
    total_qna : int = 0
    
    class Settings:
        name = "users"  # MongoDB collection name

    # Optional: You can use this to convert to a dictionary if needed
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "documents": [str(doc_id) for doc_id in self.documents]  # Convert ObjectId to string
        }
