from fastapi import APIRouter
from app.routes import auth_routes, upload_routes, document_routes, profile_routes, qna_routes
include_routers = APIRouter()

include_routers.include_router(auth_routes.router, prefix="/api", tags=["Auth"])
include_routers.include_router(upload_routes.router, prefix="/api", tags=["Upload"])
include_routers.include_router(document_routes.router, prefix="/api", tags=["Documents"])
include_routers.include_router(profile_routes.router, prefix="/api", tags=["Profile"])
include_routers.include_router(qna_routes.router, prefix="/api", tags=["QnA"])