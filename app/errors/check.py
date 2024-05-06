from starlette import status

from app.errors.base import BaseError


class CheckNotFoundError(BaseError):
    def __init__(self, check_id):
        status_code = status.HTTP_404_NOT_FOUND
        detail = f"Check with id {check_id} does not exist"
        super(CheckNotFoundError, self).__init__(status_code=status_code, detail=detail)


class NotEnoughPaymentAmountError(BaseError):
    def __init__(self):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = "Not enough payment amount"
        super(NotEnoughPaymentAmountError, self).__init__(
            status_code=status_code, detail=detail
        )


class WrongPaymentTypeError(BaseError):
    def __init__(self):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = "Wrong payment type"
        super(WrongPaymentTypeError, self).__init__(
            status_code=status_code, detail=detail
        )
