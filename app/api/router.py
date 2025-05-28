from fastapi import APIRouter

from app.api.routes import admin, user, search

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(search.router, tags=["search"])
