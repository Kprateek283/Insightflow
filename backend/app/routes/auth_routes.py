from fastapi import APIRouter, HTTPException
from app.services.auth_service import login, signup
from app.schemas.auth_schema import UserSignupRequest, UserLoginRequest

router = APIRouter()

@router.post("/login")
async def login_user_route(user_login_data: UserLoginRequest):
    try:
        login_user = await login(user_login_data)
        return {"message": "Login successful", "user": login_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signup")
async def signup_user_route(user_signup_data: UserSignupRequest):
    try:
        signup_user = await signup(user_signup_data)
        return {"message": "Signup successful", "user": signup_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
