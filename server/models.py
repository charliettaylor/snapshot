from pydantic import BaseModel


class DbModel(BaseModel):
    class Config:
        orm_mode = True


class User(DbModel):
    username: str
    phone: str
    is_active: bool


class Registrations(DbModel):
    id: int
    username: str
    state: int


class Prompts(DbModel):
    id: int
    prompt: str
    week: int
    year: int
