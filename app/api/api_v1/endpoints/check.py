from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.check import CheckCreate, CheckShow
from app.services.check import CheckService
from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.filters.check import CheckFilter
from app.config import settings


router = APIRouter(tags=["Checks"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CheckShow)
async def create_check(
    request: CheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CheckService(db)
    check = await service.create_check(
        request.products, request.payment, current_user.id
    )
    return check


@router.get("/", status_code=status.HTTP_200_OK)
async def get_checks(
    check_filter: CheckFilter = FilterDepends(CheckFilter),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Page:
    service = CheckService(db)
    checks = await service.get_checks_list(current_user.id, check_filter)
    return paginate(checks)


@router.get("/{check_id}", status_code=status.HTTP_200_OK)
async def get_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CheckService(db)
    check = await service.get_check(check_id, current_user.id)
    return check


@router.get(
    "/check-text/{check_id}",
    status_code=status.HTTP_200_OK,
    response_class=PlainTextResponse,
)
async def get_text_check(
    check_id: int,
    max_row_length: Union[int, None] = settings.DEFAULT_MAX_ROW_LENGTH,
    db: AsyncSession = Depends(get_db),
):
    service = CheckService(db)
    text_check = await service.generate_text_check(
        check_id=check_id, max_row_length=max_row_length
    )
    return text_check
