from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declarative_base,
    relationship,
)


class Base(DeclarativeBase):
    __allow_unmapped__ = True


class User(Base):
    __tablename__ = "users"

    username = mapped_column(String, primary_key=True)
    phone = mapped_column(String, unique=True)
    active = mapped_column(Boolean, default=True)
    hash = mapped_column(String, unique=True)

    pics: Mapped[Optional["Pic"]] = relationship("Pic", back_populates="uploader")


class Registration(Base):
    __tablename__ = "registrations"

    phone = mapped_column(String, primary_key=True)
    username = mapped_column(String)
    state = mapped_column(Integer)


class Prompt(Base):
    __tablename__ = "prompts"

    id = mapped_column(Integer, primary_key=True)
    prompt = mapped_column(String, nullable=False)
    date = mapped_column(Date, nullable=False)

    pics: Mapped[Optional["Pic"]] = relationship("Pic", back_populates="parent")


class Pic(Base):
    __tablename__ = "pics"

    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String)
    prompt = mapped_column(Integer, ForeignKey("prompts.id"))
    user = mapped_column(String, ForeignKey("users.username"))
    winner = mapped_column(Boolean, default=False)

    parent = relationship("Prompt", back_populates="pics")
    uploader = relationship("User", back_populates="pics")
