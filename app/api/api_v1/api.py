from fastapi import APIRouter

from app.api.api_v1.endpoints import user
from app.api.api_v1.endpoints import check
from app.api.api_v1.endpoints import auth


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(check.router, prefix="/checks", tags=["Checks"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
