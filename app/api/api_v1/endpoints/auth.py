from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.jwt import Token
from app.services.auth import AuthService

router = APIRouter()


@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
async def get_access_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).get_access_token(
        request.username, request.password
    )
