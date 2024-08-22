from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, true
from sqlalchemy.orm import relationship, Mapped
from typing import Optional


from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    phone = Column(String, unique=True)
    active = Column(Boolean, default=True)
    hash = Column(String, unique=True)

    pics: Mapped[Optional["Pic"]] = relationship("Pic", back_populates="uploader")


class Registration(Base):
    __tablename__ = "registrations"

    phone = Column(String, primary_key=True)
    username = Column(String)
    state = Column(Integer)


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    pics: Mapped[Optional["Pic"]] = relationship("Pic", back_populates="parent")


class Pic(Base):
    __tablename__ = "pics"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    prompt = Column(Integer, ForeignKey("prompts.id"))
    user = Column(String, ForeignKey("users.username"))

    parent = relationship("Prompt", back_populates="pics")
    uploader = relationship("User", back_populates="pics")
