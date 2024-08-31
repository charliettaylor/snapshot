from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

import util
from models import *


class Crud:
    def get_user(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_phone(self, db: Session, phone: str) -> User | None:
        return db.query(User).filter(User.phone == phone).first()

    def get_user_by_hash(self, db: Session, hash: str) -> User | None:
        return db.query(User).filter(User.hash == hash).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, phone: str, username: str) -> User:
        user = User(
            username=username,
            phone=phone,
            active=True,
            hash=util.user_hash(username),
            pics=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_user(self, db: Session, user: User) -> User | None:
        db_user = db.query(User).filter(User.phone == user.phone).first()

        if db_user is None:
            return None

        db_user.username = user.username
        db_user.active = user.active
        db.commit()

        return db_user

    def get_reg(self, db: Session, phone: str) -> Registration | None:
        return db.query(Registration).filter(Registration.phone == phone).first()

    def create_reg(self, db: Session, phone: str) -> Registration:
        db_reg = Registration(phone=phone, state=0)
        db.add(db_reg)
        db.commit()
        db.refresh(db_reg)
        return db_reg

    def update_reg(
        db: Session, phone: str, state: int, username: Optional[int] = None
    ) -> Registration | None:
        db_reg = db.query(Registration).filter(Registration.phone == phone).first()

        if db_reg is None:
            return None

        db_reg.state = state
        if username is not None:
            db_reg.username = username
        db.commit()

        return db_reg

    def get_prompt(self, db: Session, prompt_id: int) -> Prompt | None:
        return db.query(Prompt).filter(Prompt.id == prompt_id).first()

    def get_current_prompt(self, db: Session) -> Prompt | None:
        return db.query(Prompt).order_by(Prompt.id.desc()).first()

    def create_prompt(self, db: Session, prompt_text: str):
        db_prompt = Prompt(prompt=prompt_text, date=datetime.now().date())
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        return db_prompt

    def get_pic(self, db: Session, username: str, prompt_id: int):
        return (
            db.query(Pic).filter(Pic.user == username, Pic.prompt == prompt_id).first()
        )

    def get_pics_by_hash(self, db: Session, user_hash: str) -> List[Pic]:
        user: User = db.query(User).filter(User.hash == user_hash).first()
        return db.query(Pic).filter(Pic.user == user.username)

    def get_pics_by_prompt(self, db: Session, prompt_id: int) -> List[Pic]:
        return db.query(Pic).filter(Pic.prompt == prompt_id)

    def get_submission_status(
        self, db: Session, user_hash: str, prompt_id: int
    ) -> bool:
        user = self.get_user_by_hash(db, user_hash)
        print(user_hash)
        if user is None:
            return False
        pic = self.get_pic(db, user.username, prompt_id)

        return pic is not None

    def create_pic(self, db: Session, url: str, prompt_id: int, username: str) -> Pic:
        if self.get_pic(db, username, prompt_id) is not None:
            return None

        picModel = Pic(url=url, prompt=prompt_id, user=username)

        db.add(picModel)
        db.commit()
        db.refresh(picModel)

        return picModel
