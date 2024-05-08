from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class UserShow(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str


class UserAuth(BaseModel):
    username: str
    password: str
