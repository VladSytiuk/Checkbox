from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.models import Check


class CheckFilter(Filter):
    total__gte: Optional[float] = None
    total__lte: Optional[float] = None
    created_at__gte: Optional[str] = None
    created_at__lte: Optional[str] = None
    payment_type: Optional[str] = None

    class Constants(Filter.Constants):
        model = Check
