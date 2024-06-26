from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.schemas.check import Product, Payment, CheckShow
from app.models import Check
from app.filters.check import CheckFilter
from app.errors.auth import NotEnoughPermissionError
from app.errors.check import (
    CheckNotFoundError,
    WrongPaymentTypeError,
    NotEnoughPaymentAmountError,
)
from app.config import settings
from app.storages.interfaces import CheckStorageInterface
from app.storages.postgres.check import CheckStorage


class CheckService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.check_storage: CheckStorageInterface = CheckStorage(self.db)

    async def create_check(
        self, products: list[Product], payment: Payment, user_id: int
    ) -> Check:
        products_data = self._get_products_data(products)
        check_total = self._calculate_check_total(products_data)

        self._validate_payment(payment=payment, total=check_total)

        rest = abs(check_total - payment.amount)
        check = await self.check_storage.create_check(
            products=products_data,
            payment=payment,
            user_id=user_id,
            total=check_total,
            rest=rest,
        )
        return check

    async def get_checks_list(
        self, user_id: int, check_filter: CheckFilter
    ) -> list[CheckShow]:
        checks_list = await self.check_storage.get_checks_list(
            user_id=user_id, check_filter=check_filter
        )
        return checks_list

    async def get_check(self, check_id: int, user_id: int) -> Check:
        check, check_owner_id = await self.check_storage.get_check_by_id(
            check_id=check_id
        )
        if not check:
            raise CheckNotFoundError(check_id)
        if check_owner_id != user_id:
            raise NotEnoughPermissionError()
        return check

    @staticmethod
    def _validate_payment(payment: Payment, total: float) -> None:
        if payment.type not in settings.ALLOWED_PAYMENT_TYPE:
            raise WrongPaymentTypeError()
        if payment.amount - total < 0:
            raise NotEnoughPaymentAmountError()

    @staticmethod
    def _get_products_data(products: list[Product]) -> list[dict]:
        products_data = []
        for product in products:
            product_total = product.price * product.quantity
            products_data.append(
                {
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity,
                    "total": product_total,
                }
            )
        return products_data

    @staticmethod
    def _calculate_check_total(products: list[dict]) -> float:
        return sum([product["total"] for product in products])

    async def _get_check_by_id(self, check_id) -> Check:
        query = await self.db.execute(select(Check).where(Check.id == check_id))
        check = query.scalars().first()
        if not check:
            raise CheckNotFoundError(check_id)
        return check

    async def generate_text_check(
        self, check_id: int, max_row_length: int
    ) -> str:
        lines = []
        check, user_id = await self.check_storage.get_check_by_id(
            check_id=check_id
        )
        # Function to format price with commas for thousands separator

        def format_price(price: float):
            return f"{price:,.2f}".replace(",", " ")

        # Function to format quantity with spaces for alignment
        def format_quantity(quantity: int):
            return f"{quantity:.2f}".replace(".", " ")

        # Add company name
        lines.append("Checkbox".center(max_row_length))

        # Add horizontal line
        lines.append("=" * max_row_length)

        # Add products
        for product in check.products:
            name = product.name
            quantity = product.quantity
            price = product.price
            product_total = product.total

            # Format product data
            product_data = (
                f"{format_quantity(quantity)} x {format_price(price)}"
            )
            product_line_1 = product_data.ljust(max_row_length)
            product_line_2 = (
                f"{name.ljust(max_row_length - len(format_price(product_total)))}"
                f"{format_price(product_total)}".rjust(max_row_length)
            )

            # Add product lines
            lines.append(product_line_1)
            lines.append(product_line_2)

            # Add separator
            lines.append("-" * max_row_length)

        # Remove the last unnecessary separator
        lines.pop()
        lines.append("=" * max_row_length)

        # Calculate the space needed to align totals
        total_space = max_row_length - 6  # Space for "Total"
        payment_space = max_row_length - 8  # Space for "Payment"
        rest_space = max_row_length - 5  # Space for "Rest"

        # Add total
        total_line = f"Total {format_price(check.total): >{total_space}}"
        lines.append(total_line)

        # Add payment
        payment_line = (
            f"Payment {format_price(check.payment.amount): >{payment_space}}"
        )
        lines.append(payment_line)

        # Add rest
        rest_line = f"Rest {format_price(check.rest): >{rest_space}}"
        lines.append(rest_line)

        # Add horizontal line
        lines.append("=" * max_row_length)

        # Add timestamp
        lines.append(f"{str(check.created_at).center(max_row_length)}")
        # Add closing message
        lines.append("Thanks for buying".center(max_row_length))

        return "\n".join(lines)
