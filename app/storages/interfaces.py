from abc import ABC, abstractmethod

from app.schemas.user import UserCreate, UserShow, UserAuth
from app.schemas.check import Payment, CheckShow
from app.filters.check import CheckFilter


class UserStorageInterface(ABC):

    @abstractmethod
    def create_user(self, user_data: UserCreate):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserShow:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserShow:
        pass

    @abstractmethod
    def get_user_with_password(self, username: str) -> UserAuth:
        pass


class CheckStorageInterface(ABC):

    @abstractmethod
    def create_check(
        self,
        products: dict,
        payment: Payment,
        user_id: int,
        total: float,
        rest: float,
    ) -> CheckShow:
        pass

    @abstractmethod
    def get_check_by_id(self, check_id: int) -> tuple[CheckShow, int]:
        pass

    @abstractmethod
    def get_checks_list(
        self, user_id: int, check_filter: CheckFilter
    ) -> list[CheckShow]:
        pass
