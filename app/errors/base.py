class BaseError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.code = status_code
        self.detail = detail
