from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storages.interfaces import UserStorageInterface
from app import models
from app.schemas.user import UserCreate, UserShow, UserAuth
from app.hashing import get_password_hash


class UserStorage(UserStorageInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate):

        hashed_password = get_password_hash(user_data.password)
        new_user = models.User(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=hashed_password,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

    async def get_user_by_id(self, user_id: int) -> UserShow:
        query = await self.db.execute(
            select(models.User).where(models.User.id == user_id)
        )
        user = query.scalars().first()
        return UserShow(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

    async def get_user_by_username(self, username: str) -> UserShow:
        query = await self.db.execute(
            select(models.User).where(models.User.username == username)
        )
        user = query.scalars().first()
        if user:
            return UserShow(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )

    async def get_user_with_password(self, username: str) -> UserAuth:
        query = await self.db.execute(
            select(models.User).where(models.User.username == username)
        )
        user = query.scalars().first()
        return UserAuth(username=user.username, password=user.password)
