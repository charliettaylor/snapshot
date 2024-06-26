import datetime
from typing import List

from click import prompt
import models, schema
from sqlalchemy.orm import Session
from fastapi import UploadFile


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_phone(db: Session, phone: str) -> models.User | None:
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_user_by_hash(db: Session, hash: str) -> models.User | None:
    return db.query(models.User).filter(models.User.hash == hash).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.User) -> models.User:
    db_user = models.User(username=user.username, phone=user.phone, active=True, hash=user.hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schema.User) -> models.User | None:
    db_user = (
        db.query(models.User)
        .filter(models.User.phone == user.phone)
        .first()
    )

    if db_user is None:
        return None

    db_user.username = user.username
    db_user.active = user.active
    db.commit()

    return db_user

def get_reg(db: Session, phone: str) -> models.Registration | None:
    return (
        db.query(models.Registration).filter(models.Registration.phone == phone).first()
    )


def create_reg(db: Session, phone: str) -> models.Registration:
    db_reg = models.Registration(phone=phone, state=0)
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg


def update_reg(db: Session, reg: schema.Registration) -> models.Registration | None:
    db_reg = (
        db.query(models.Registration)
        .filter(models.Registration.phone == reg.phone)
        .first()
    )

    if db_reg is None:
        return None

    db_reg.username = reg.username  # type: ignore
    db_reg.state = reg.state  # type: ignore
    db.commit()

    return db_reg


def get_current_prompt(db: Session) -> models.Prompt | None:
    week, year = get_week_year()
    return db.query(models.Prompt).filter_by(week=week, year=year).first()


def create_pic(db: Session, username: str, file: UploadFile):
    p = get_current_prompt(db)
    pic = models.Pic(data=file.file, prompt=file.content_type, user=username, prompt=p)


def get_week_year() -> tuple[int, int]:
    year, week, _ = datetime.date.today().isocalendar()
    return week, year
