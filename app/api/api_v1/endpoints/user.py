from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User
from app.services.user import UserService
from app.api.dependencies import get_db


router = APIRouter(tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: User, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(request)
