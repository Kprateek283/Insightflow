from app.database.db import get_db
from app.models.user_model import User
from app.schemas.auth_schema import UserResponse
from bson import ObjectId

# Ensure to await get_db and use the database connection
async def create_user(user_data: User) -> UserResponse:
    db = await get_db()  # Await the database connection
    user_collection = db["users"]
    user_dict = user_data.model_dump(exclude_unset=True)  # Use Pydantic's dict method
    result = await user_collection.insert_one(user_dict)

    return UserResponse(
        id=str(user_data.id),
        name=user_data.name,
        email=user_data.email,
        token=None,
        created_at=user_data.created_at,
        documents=user_data.documents or []  # Ensure documents are included if necessary
    )

async def get_user_by_email(email: str) -> User:
    db = await get_db() 
    user_collection = db["users"]
    user_data = await user_collection.find_one({"email": email})
    if user_data:
        user_data["id"] = str(user_data.pop("_id"))
        return User(**user_data)
    return None

async def get_user_by_id(user_id: str) -> User:
    db = await get_db()  # Await the database connection
    user_collection = db["users"]
    user_data = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data.pop("_id"))
        return User(**user_data)
    return None
