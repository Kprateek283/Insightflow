import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from contextlib import asynccontextmanager

from app.routes.include_routers import include_routers
from app.middlewares.auth_middleware import AuthMiddleware  # assuming you have this
from app.database.db import connect_to_mongo, disconnect_from_mongo
from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env file

ENV = os.getenv("ENV", "development") 

dev = ENV == "development"

origins = ["*"] if dev else [
    os.getenv("FRONTEND_URL", "https://your-frontend.vercel.app")
]

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await disconnect_from_mongo()

# Combined middleware list
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(
        AuthMiddleware,
        skip_paths=[
            "/", "/publichealth", "/api/login", "/api/signup", "/docs", "/openapi.json"
        ]
    )
]

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan, middleware=middleware)

# Include your routers
app.include_router(include_routers)

# Basic routes
@app.get("/")
def root():
    return {"message": "Welcome to the MongoDB-connected FastAPI app!"}

@app.get("/publichealth")
async def public_health_check():
    return {"status": "Public Route healthy"}

@app.get("/protectedhealth")
async def protected_health_check():
    return {"status": "Protected Route healthy"}
