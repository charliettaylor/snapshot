from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    phone = Column(String, unique=True)
    is_active = Column(Boolean, default=True)


class Registrations(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    state = Column(Integer)


class Prompts(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    week = Column(Integer, nullable=False)
    prompt = Column(Integer, nullable=False)
