import stat
from typing import List
import models, schema
from sqlalchemy.orm import Session


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_phone(db: Session, phone: str) -> models.User | None:
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.User) -> models.User:
    db_user = models.User(username=user.username, phone=user.phone, active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_reg(db: Session, phone: str) -> models.Registration | None:
    return (
        db.query(models.Registration).filter(models.Registration.phone == phone).first()
    )


def create_reg(db: Session, phone: str ) -> models.Registration:
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

    db_reg.username = reg.username
    db_reg.state = reg.state
    db.commit()

    return db_reg
