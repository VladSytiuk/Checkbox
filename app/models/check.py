from sqlalchemy import (
    Column,
    String,
    Integer,
    JSON,
    DateTime,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="checks")
    products = Column(JSON)
    payment_type = Column(String)
    payment_amount = Column(Numeric(10, 2))
    created_at = Column(DateTime)
    total = Column(Numeric(10, 2))
    rest = Column(Numeric(10, 2))
