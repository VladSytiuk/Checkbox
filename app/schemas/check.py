from datetime import datetime
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    total: float = 0


class Payment(BaseModel):
    type: str
    amount: float


class CheckCreate(BaseModel):

    products: list[Product]
    payment: Payment


class CheckShow(CheckCreate):

    id: int
    total: float
    rest: float
    created_at: datetime
