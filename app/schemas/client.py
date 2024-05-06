from pydantic import BaseModel
from datetime import date


class Client(BaseModel):
    category: str
    firstname: str
    lastname: str
    email: str
    gender: str
    birthDate: date
