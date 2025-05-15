import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import os

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, skip_paths=None):
        super().__init__(app)
        self.skip_paths = set(skip_paths or [])
        self.secret_key = os.getenv("JWT_SECRET")
        self.algorithm = os.getenv("JWT_ALGORITHM")

    async def dispatch(self, request: Request, call_next):
        path = request.url.path.rstrip("/")

        if path in self.skip_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Missing or malformed token"}, status_code=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            request.state.user = payload 
        except ExpiredSignatureError:
            return JSONResponse({"error": "Token expired"}, status_code=401)
        except InvalidTokenError:
            return JSONResponse({"error": "Invalid token"}, status_code=401)

        return await call_next(request)
