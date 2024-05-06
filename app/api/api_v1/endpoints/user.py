from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import User
from app.services.user import UserService
from app.api.dependencies import get_db


router = APIRouter(tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(request)
