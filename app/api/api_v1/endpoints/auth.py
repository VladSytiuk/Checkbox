from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.jwt import Token
from app.services.auth import AuthService

router = APIRouter()


@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def get_access_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return AuthService(db).get_access_token(request.username, request.password)
