from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.jwt import TokenData
from app.config import settings
from app.errors.auth import UserNotAuthenticatedError
from app.db.session import async_session
from app.storages.interfaces import UserStorageInterface
from app.storages.postgres.user import UserStorage


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_db():
    async with async_session() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    user_storage: UserStorageInterface = UserStorage(db)
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
    user = await user_storage.get_user_by_username(username=token_data.username)
    return user
