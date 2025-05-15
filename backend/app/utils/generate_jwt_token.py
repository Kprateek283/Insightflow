from datetime import datetime, timedelta, timezone
from app.models.user_model import User
import os
from dotenv import load_dotenv
from jose import jwt

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

def generate_jwt_token(user: User) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(days=1)
    
    payload = {
        "sub": str(user.id),  # Convert ObjectId to string
        "name": user.name,  # Assuming name is always a string
        "email": user.email,  # Assuming email is always a string
        "exp": int(expiration.timestamp()),  # JWT expects timestamp
        "iat": int(datetime.now(timezone.utc).timestamp())
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
