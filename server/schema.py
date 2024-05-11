from pydantic import BaseModel
from typing import List


class DbModel(BaseModel):
    class Config:
        from_attributes = True


class Pic(DbModel):
    id: int
    data: bytes
    format: str
    prompt: int
    user: str


class User(DbModel):
    username: str
    phone: str
    active: bool
    hash: str

    pics: List[Pic] | None


class Registration(DbModel):
    phone: str
    username: str | None
    state: int


class Prompt(DbModel):
    id: int
    prompt: str
    week: int
    year: int

    pics: List[Pic] | None
