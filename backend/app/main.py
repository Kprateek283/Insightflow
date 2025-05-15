import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from app.routes.include_routers import include_routers
from app.middlewares.auth_middleware import AuthMiddleware
from app.database.db import connect_to_mongo, disconnect_from_mongo
from dotenv import load_dotenv

load_dotenv()

# 1. Load frontend URL from env or fallback for debugging
frontend_url = os.getenv("FRONTEND_URL", "https://insightfloww.vercel.app")
origins = [frontend_url]

# 2. CORS must be placed before any custom blocking middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        AuthMiddleware,
        skip_paths=[
            "/", "/publichealth", "/api/login", "/api/signup", "/docs", "/openapi.json"
        ]
    )
]

# 3. Lifecycle hooks for DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await disconnect_from_mongo()

# 4. App initialization
app = FastAPI(lifespan=lifespan, middleware=middleware)

# 5. Logging origin header (for debugging on Render)
@app.middleware("http")
async def log_origin(request: Request, call_next):
    print("Incoming Origin:", request.headers.get("origin"))
    response = await call_next(request)
    return response

# 6. Explicit OPTIONS route to test preflight (optional but helps debugging)
@app.options("/api/login")
async def preflight_login():
    return JSONResponse(content={"message": "Preflight OK"})

# 7. Mount your routers
app.include_router(include_routers)

# 8. Public test routes
@app.get("/")
def root():
    return {"message": "Welcome to the MongoDB-connected FastAPI app!"}

@app.get("/publichealth")
async def public_health_check():
    return {"status": "Public Route healthy"}

@app.get("/protectedhealth")
async def protected_health_check():
    return {"status": "Protected Route healthy"}
