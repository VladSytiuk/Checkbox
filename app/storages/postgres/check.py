from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storages.interfaces import CheckStorageInterface
from app.models import Check
from app.schemas.check import Payment, CheckShow
from app.filters.check import CheckFilter


class CheckStorage(CheckStorageInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_check(
        self,
        products: dict,
        payment: Payment,
        user_id: int,
        total: float,
        rest: float,
    ) -> CheckShow:
        check = Check(
            user_id=user_id,
            products=products,
            payment_type=payment.type,
            payment_amount=payment.amount,
            total=total,
            rest=rest,
            created_at=datetime.now(),
        )
        self.db.add(check)
        await self.db.commit()
        return CheckShow(
            id=check.id,
            products=check.products,
            payment=payment,
            total=check.total,
            rest=check.rest,
            created_at=check.created_at,
        )

    async def get_check_by_id(self, check_id: int) -> tuple[CheckShow, int]:
        query = await self.db.execute(select(Check).where(Check.id == check_id))
        check = query.scalars().first()
        payment = Payment(type=check.payment_type, amount=check.payment_amount)
        check_show = CheckShow(
            id=check.id,
            products=check.products,
            payment=payment,
            total=check.total,
            rest=check.rest,
            created_at=check.created_at,
        )
        return check_show, check.user_id

    async def get_checks_list(
        self, user_id: int, check_filter: CheckFilter
    ) -> list[CheckShow]:
        query = await self.db.execute(
            check_filter.filter(select(Check).where(Check.user_id == user_id))
        )
        checks = query.scalars().all()
        checks_list = []
        for check in checks:
            payment = Payment(
                type=check.payment_type, amount=check.payment_amount
            )
            checks_list.append(
                CheckShow(
                    id=check.id,
                    products=check.products,
                    payment=payment,
                    total=check.total,
                    rest=check.rest,
                    created_at=check.created_at,
                )
            )
        return checks_list
