from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.auth_schema import UserSignupRequest, UserResponse, UserLoginRequest
from app.utils.hash_password import hash_password
from datetime import datetime, timezone
from app.database.user_db import create_user, get_user_by_email
from app.utils.generate_jwt_token import generate_jwt_token
from app.utils.verify_password import verify_password

async def signup(user_signup_data: UserSignupRequest) -> UserResponse:
    # Hash the password
    hashed_password = hash_password(user_signup_data.password)
    
    # Create user instance without token
    user_data = User(
        name=user_signup_data.name,
        email=user_signup_data.email,
        password=hashed_password,
        created_at=datetime.now(timezone.utc)
    )

    # Check if the user already exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create the user in the database
    new_user = await create_user(user_data)

    # Return the user response without the token
    return UserResponse(
        id=str(new_user.id),  # Ensure id is a string (if ObjectId)
        name=new_user.name,
        email=new_user.email,
        token=None,  # No token during signup
        created_at=new_user.created_at,
        documents=new_user.documents or []  # Ensure documents are included if necessary
    )

async def login(user_login_data: UserLoginRequest) -> UserResponse:
    # Get the user by email
    login_user = await get_user_by_email(user_login_data.email)
    if not login_user:
        raise HTTPException(status_code=400, detail="Invalid Email")

    # Verify the password
    if not verify_password(user_login_data.password, login_user.password):
        raise HTTPException(status_code=400, detail="Invalid Password")
    
    # Generate JWT token
    token = generate_jwt_token(login_user)

    # Convert user data to dictionary and return UserResponse
    user_dict = login_user.to_dict()
    
    return UserResponse(
        id=user_dict["id"],
        name=user_dict["name"],
        email=user_dict["email"],
        token=token,
        created_at=user_dict["created_at"]
    )
