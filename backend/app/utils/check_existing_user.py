from typing import Optional
from app.models.user_model import User
from app.database.db import get_db

async def get_user_by_email(email: str) -> Optional[User]:
    db = await get_db()
    user_collection = db["users"]
    user_doc = await user_collection.find_one({"email": email})
    if user_doc:
        user_doc["id"] = str(user_doc["_id"])  # Convert MongoDB ObjectId
        return User(**user_doc)
    return None
