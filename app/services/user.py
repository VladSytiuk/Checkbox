from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate
from app.services.base import BaseService
from app.errors.user import UserAlreadyExistError
from app.storages.interfaces import UserStorageInterface
from app.storages.postgres.user import UserStorage


class UserService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.user_storage: UserStorageInterface = UserStorage(self.db)

    async def create_user(self, request: UserCreate) -> str:
        user = await self.user_storage.get_user_by_username(request.username)
        if user:
            raise UserAlreadyExistError(username=user.username)
        await self.user_storage.create_user(request)
        return f"User with username {request.username} has been created successfully"
