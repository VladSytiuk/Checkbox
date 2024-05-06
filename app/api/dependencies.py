from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.schemas.jwt import TokenData
from app.models import User
from app.config import settings
from app.errors.auth import UserNotAuthenticatedError
from app.db.session import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise UserNotAuthenticatedError()
        token_data = TokenData(username=username)
    except JWTError:
        raise UserNotAuthenticatedError()
    user = db.query(User).filter(User.username == token_data.username).first()
    return user
