from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.db.session import Base, engine
from app.api.api_v1.api import api_router
from app.errors.base import BaseError


app = FastAPI()

Base.metadata.create_all(bind=engine)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Checkbox API",
        version="1.0.0",
        description="""Checkbox API allows to create and authenticate users,
        create get and filter checks, generate text representation of check.                      
                    """,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(api_router)

add_pagination(app)


@app.exception_handler(BaseError)
async def custom_exception_handler(_: Request, exc: BaseError):
    return JSONResponse(status_code=exc.code, content={"detail": exc.detail})
