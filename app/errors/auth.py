from starlette import status

from app.errors.base import BaseError


class UserNotAuthenticatedError(BaseError):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Not authenticated"
        super(UserNotAuthenticatedError, self).__init__(
            status_code=status_code, detail=detail
        )


class NotEnoughPermissionError(BaseError):
    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN
        detail = "Not enough permission"
        super(NotEnoughPermissionError, self).__init__(
            status_code=status_code, detail=detail
        )


class InvalidCredentialsError(BaseError):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Invalid username or password"
        super(InvalidCredentialsError, self).__init__(
            status_code=status_code, detail=detail
        )
