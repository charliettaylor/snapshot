from pydantic import BaseModel


class DbModel(BaseModel):
    class Config:
        from_attributes = True


class User(DbModel):
    username: str
    phone: str
    is_active: bool


class Registration(DbModel):
    phone: str
    username: str
    state: int


class Prompt(DbModel):
    id: int
    prompt: str
    week: int
    year: int
