from sqlalchemy import select

from app import models
from app.schemas.user import User
from app.hashing import get_password_hash
from app.services.base import BaseService
from app.errors.user import UserAlreadyExistError


class UserService(BaseService):

    async def create_user(self, request: User) -> str:
        query = await self.db.execute(
            select(models.User).where(models.User.username == request.username)
        )
        user = query.scalars().first()
        if user:
            raise UserAlreadyExistError(username=user.username)
        hashed_password = get_password_hash(request.password)
        new_user = models.User(
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            password=hashed_password,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return f"User with username {request.username} has been created successfully"
