from pydantic import BaseModel


class DbModel(BaseModel):
    class Config:
        from_attributes = True


class User(DbModel):
    username: str
    phone: str
    is_active: bool


class Registrations(DbModel):
    phone: str
    username: str
    state: int


class Prompts(DbModel):
    id: int
    prompt: str
    week: int
    year: int
