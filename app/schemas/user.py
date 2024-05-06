from pydantic import BaseModel, field_validator


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
