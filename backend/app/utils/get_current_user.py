from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from app.database.user_db import get_user_by_email
from app.schemas.auth_schema import UserResponse
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

async def get_current_user(request: Request) -> UserResponse:
    token = None

    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    # If not found in header, try to get from form (multipart)
    if not token and request.headers.get("Content-Type", "").startswith("multipart/form-data"):
        form = await request.form()
        token = form.get("token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token missing or invalid")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        print(payload.get("email"))
        user_email: str = payload.get("email")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token payload invalid")

        user = await get_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current User not found")

        return user

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
