from collections.abc import Generator
from datetime import datetime

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


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Database:
    def __init__(self):
        db = next(get_db(), None)
        if db is None:
            raise Exception("Could not connect to database")
        self.db: Session = db

    def get_user(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_phone(self, phone: str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    def get_user_by_hash(self, hash: str) -> User | None:
        return self.db.query(User).filter(User.hash == hash).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
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
        db_user = self.db.query(User).filter(User.phone == user.phone).first()

        if db_user is None:
            return None

        db_user.username = user.username
        db_user.active = user.active
        self.db.commit()

        return db_user

    def get_reg(self, phone: str) -> Registration | None:
        return self.db.query(Registration).filter(Registration.phone == phone).first()

    def create_reg(self, phone: str) -> Registration:
        db_reg = Registration(phone=phone, state=0)
        self.db.add(db_reg)
        self.db.commit()
        self.db.refresh(db_reg)
        return db_reg

    def update_reg(
        self, phone: str, state: int, username: str | None = None
    ) -> Registration | None:
        db_reg = self.db.query(Registration).filter(Registration.phone == phone).first()

        if db_reg is None:
            return None

        db_reg.state = state  # pyright: ignore [reportAttributeAccessIssue]
        if username is not None:
            db_reg.username = username  # pyright: ignore [reportAttributeAccessIssue]
        self.db.commit()

        return db_reg

    def get_prompt(self, prompt_id: int) -> Prompt | None:
        return self.db.query(Prompt).filter(Prompt.id == prompt_id).first()

    def get_current_prompt(self) -> Prompt | None:
        return self.db.query(Prompt).order_by(Prompt.id.desc()).first()

    def create_prompt(self, prompt_text: str):
        db_prompt = Prompt(prompt=prompt_text, date=datetime.now().date())
        self.db.add(db_prompt)
        self.db.commit()
        self.db.refresh(db_prompt)
        return db_prompt

    def get_all_prompts(self) -> list[Prompt]:
        return self.db.query(Prompt).all()

    def get_pic(self, username: str, prompt_id: int):
        return (
            self.db.query(Pic)
            .filter(Pic.user == username, Pic.prompt == prompt_id)
            .first()
        )

    def get_pics_by_hash(self, user_hash: str) -> list[Pic]:
        user = self.db.query(User).filter(User.hash == user_hash).first()
        if user is None:
            return []
        return list(self.db.query(Pic).filter(Pic.user == user.username))

    def get_pics_by_prompt(self, prompt_id: int) -> list[Pic]:
        return list(
            self.db.query(Pic)
            .filter(Pic.prompt == prompt_id)
            .order_by(Pic.winner.desc())
        )

    def get_winner_by_prompt(self, prompt_id: int) -> Pic | None:
        return (
            self.db.query(Pic)
            .filter(Pic.prompt == prompt_id, Pic.winner == True)
            .first()
        )

    def get_submission_status(self, user_hash: str, prompt_id: int) -> bool:
        user = self.get_user_by_hash(user_hash)
        if user is None:
            return False
        pic = self.get_pic(str(user.username), prompt_id)

        return pic is not None

    def create_pic(self, url: str, prompt_id: int, username: str) -> Pic | None:
        if self.get_pic(username, prompt_id) is not None:
            return None

        pic = Pic(url=url, prompt=prompt_id, user=username)

        self.db.add(pic)
        self.db.commit()
        self.db.refresh(pic)

        return pic

    def set_winner(self, pic_id: int):
        pic = self.db.query(Pic).filter(Pic.id == pic_id).first()

        if pic is None:
            return None

        pic.winner = not pic.winner  # pyright: ignore [reportAttributeAccessIssue]
        self.db.commit()
        return pic
