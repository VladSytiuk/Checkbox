from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.models import User
from app.services.base import BaseService
from app.hashing import verify_password
from app.config import settings
from app.errors.auth import InvalidCredentialsError


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


class AuthService(BaseService):

    def get_access_token(self, username: str, password: str) -> dict:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError()
        access_token = self.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
