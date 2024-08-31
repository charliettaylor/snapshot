from datetime import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import util
from config import settings
from models import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./" + settings.db_name

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Database:
    def __init__(self):
        self.db: Session = next(get_db(), None)
        if self.db is None:
            raise Exception("Could not connect to database")

    def get_user(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_phone(self, phone: str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    def get_user_by_hash(self, hash: str) -> User | None:
        return self.db.query(User).filter(User.hash == hash).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, phone: str, username: str) -> User:
        user = User(
            username=username,
            phone=phone,
            active=True,
            hash=util.user_hash(username),
            pics=None,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User) -> User | None:
        self.db_user = self.db.query(User).filter(User.phone == user.phone).first()

        if self.db_user is None:
            return None

        self.db_user.username = user.username
        self.db_user.active = user.active
        self.db.commit()

        return self.db_user

    def get_reg(self, phone: str) -> Registration | None:
        return self.db.query(Registration).filter(Registration.phone == phone).first()

    def create_reg(self, phone: str) -> Registration:
        self.db_reg = Registration(phone=phone, state=0)
        self.db.add(self.db_reg)
        self.db.commit()
        self.db.refresh(self.db_reg)
        return self.db_reg

    def update_reg(
        self, phone: str, state: int, username: Optional[int] = None
    ) -> Registration | None:
        self.db_reg = (
            self.db.query(Registration).filter(Registration.phone == phone).first()
        )

        if self.db_reg is None:
            return None

        self.db_reg.state = state
        if username is not None:
            self.db_reg.username = username
        self.db.commit()

        return self.db_reg

    def get_prompt(self, prompt_id: int) -> Prompt | None:
        return self.db.query(Prompt).filter(Prompt.id == prompt_id).first()

    def get_current_prompt(self) -> Prompt | None:
        return self.db.query(Prompt).order_by(Prompt.id.desc()).first()

    def create_prompt(self, prompt_text: str):
        self.db_prompt = Prompt(prompt=prompt_text, date=datetime.now().date())
        self.db.add(self.db_prompt)
        self.db.commit()
        self.db.refresh(self.db_prompt)
        return self.db_prompt

    def get_all_prompts(self) -> List[Prompt]:
        return self.db.query(Prompt).all()

    def get_pic(self, username: str, prompt_id: int):
        return (
            self.db.query(Pic)
            .filter(Pic.user == username, Pic.prompt == prompt_id)
            .first()
        )

    def get_pics_by_hash(self, user_hash: str) -> List[Pic]:
        user: User = self.db.query(User).filter(User.hash == user_hash).first()
        return self.db.query(Pic).filter(Pic.user == user.username)

    def get_pics_by_prompt(self, prompt_id: int) -> List[Pic]:
        return (
            self.db.query(Pic)
            .filter(Pic.prompt == prompt_id)
            .order_by(Pic.winner.desc())
        )

    def get_submission_status(self, user_hash: str, prompt_id: int) -> bool:
        user = self.get_user_by_hash(user_hash)
        print(user_hash)
        if user is None:
            return False
        pic = self.get_pic(user.username, prompt_id)

        return pic is not None

    def create_pic(self, url: str, prompt_id: int, username: str) -> Pic:
        if self.get_pic(self.db, username, prompt_id) is not None:
            return None

        picModel = Pic(url=url, prompt=prompt_id, user=username)

        self.db.add(picModel)
        self.db.commit()
        self.db.refresh(picModel)

        return picModel

    def set_winner(self, pic_id: int):
        pic = self.db.query(Pic).filter(Pic.id == pic_id).first()

        if pic is None:
            return None

        pic.winner = not pic.winner
        self.db.commit()
        return pic
