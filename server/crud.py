import datetime
from typing import List

from click import prompt
import models
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


def create_user(db: Session, user: models.User) -> models.User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: models.User) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.phone == user.phone).first()

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


def update_reg(db: Session, reg: models.Registration) -> models.Registration | None:
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


def get_prompt(db: Session, prompt_id: int) -> models.Prompt | None:
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()


def get_current_prompt(db: Session) -> models.Prompt | None:
    return db.query(models.Prompt).order_by(models.Prompt.id.desc()).first()


def create_prompt(db: Session, prompt_text: str):
    db_prompt = models.Prompt(prompt=prompt_text)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_pic(db: Session, username: str, prompt_id: int):
    return (
        db.query(models.Pic)
        .filter(models.Pic.user == username and models.Pic.id == prompt_id)
        .first()
    )


def get_pics_by_hash(db: Session, user_hash: str) -> List[models.Pic]:
    user: models.User = (
        db.query(models.User).filter(models.User.hash == user_hash).first()
    )
    return db.query(models.Pic).filter(models.Pic.user == user.username)


def get_pics_by_prompt(db: Session, prompt_id: int) -> List[models.Pic]:
    return db.query(models.Pic).filter(models.Pic.prompt == prompt_id)


def get_submission_status(db: Session, user_hash: str, prompt_id: int) -> bool:
    user = get_user_by_hash(db, user_hash)
    if user is None:
        return False
    pic = (
        db.query(models.Pic)
        .filter(models.Pic.user == user.username and models.Pic.prompt == prompt_id)
        .first()
    )

    print(pic)
    return pics is not None


def create_pic(db: Session, url: str, prompt_id: int, username: str) -> models.Pic:
    if get_pic(db, username, prompt_id) is not None:
        return None

    picModel = models.Pic(url=url, prompt=prompt_id, user=username)

    db.add(picModel)
    db.commit()
    db.refresh(picModel)

    return picModel
