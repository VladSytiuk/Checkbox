from starlette import status

from app.errors.base import BaseError


class UserAlreadyExistError(BaseError):
    def __init__(self, username: str):
        status_code = status.HTTP_409_CONFLICT
        detail = f"User with username {username} already exist"
        super(UserAlreadyExistError, self).__init__(
            status_code=status_code, detail=detail
        )
