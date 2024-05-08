from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.hashing import verify_password
from app.config import settings
from app.errors.auth import InvalidCredentialsError
from app.storages.postgres.user import UserStorage
from app.storages.interfaces import UserStorageInterface


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


class AuthService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.user_storage: UserStorageInterface = UserStorage(self.db)

    async def get_access_token(self, username: str, password: str) -> dict:
        user = await self.user_storage.get_user_with_password(username=username)
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError()
        access_token = await self.create_access_token(
            data={"sub": user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def create_access_token(
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
