from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    phone = Column(String, unique=True)
    active = Column(Boolean, default=True)
    hash = Column(String, nullable=False)


class Registration(Base):
    __tablename__ = "registrations"

    phone = Column(String, primary_key=True)
    username = Column(String)
    state = Column(Integer)


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    week = Column(Integer, nullable=False)
    prompt = Column(Integer, nullable=False)
