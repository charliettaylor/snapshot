from abc import ABC, abstractmethod

import logging

from database import get_db
from models import Registration, User
from config import settings
from crud import *
from constants import *
from util import *

logger = logging.getLogger(__name__)


class TextInterface(ABC):
    def __init__(self):
        self.db = next(get_db(), None)

    @abstractmethod
    def send_message(self, to: str, text: str):
        pass

    @abstractmethod
    def receive_message(self, from_: str, text: str):
        pass

    def handle_message(self, from_: str, text: str):
        logger.info("handle_message %s %s", from_, text)

        if settings.admin_pass in text:
            self.handle_admin_message(text)
            return

        reg = get_reg(self.db, from_)
        logger.info(
            "handle_message reg %s", vars(reg) if reg is not None else str(reg)
        )
        if reg is None:
            logger.info("handle_message create_reg %s", from_)
            reg = create_reg(self.db, from_)

        user = get_user_by_phone(self.db, from_)
        logger.info(
            "handle_message user %s", vars(user) if user is not None else str(user)
        )

        if contains(text, STOP_KEYWORDS):
            if user is not None:
                update_user(
                    self.db,
                    User(
                        phone=user.phone,
                        username=user.username,
                        active=False,
                        hash=user.hash,
                    ),
                )
            self.send_message(from_, UNSUBSCRIBED)

        elif reg.state == 0 and contains(text, START_KEYWORDS):
            update_reg(self.db, from_, 1)
            self.send_message(from_, ENTER_USERNAME)

        elif reg.state == 0:
            self.send_message(from_, HOW_TO_START)

        elif reg.state == 1:
            if not util.validate_username(text):
                self.send_message(from_, BAD_USERNAME)
                return
            update_reg(self.db, from_, 2, text)

            self.send_message(from_, CONFIRM_USERNAME.format(text))

        elif reg.state == 2 and contains(text, POSITIVE_KEYWORDS):
            create_user(self.db, from_, reg.username)
            update_reg(self.db, from_, 3, reg.username)
            self.send_message(from_, REGISTRATION_SUCCESSFUL.format(reg.username))
            prompt = get_current_prompt(self.db)
            if prompt is not None:
                self.send_prompt(from_, prompt.prompt)

        elif reg.state == 2 and contains(text, NEGATIVE_KEYWORDS):
            update_reg(self.db, from_, 1)
            self.send_message(from_, ENTER_USERNAME_AGAIN)

    def handle_image(self, from_: str, url: str):
        logger.info("handle_image %s %s", from_, url)

        user = get_user_by_phone(self.db, from_)

        if user is None:
            self.send_message(from_, INVALID_USER)
            return

        prompt = get_current_prompt(self.db)

        exists = get_submission_status(self.db, user.hash, prompt.id)

        if exists:
            self.send_message(from_, ALREADY_SUBMITTED)
            return

        pic = create_pic(self.db, url, prompt.id, user.username)

        if pic is None:
            self.send_message(from_, FAILED_PIC_SAVE)
        else:
            self.send_message(
                from_, VIEW_SUBMISSIONS.format(self.generate_url(user.hash))
            )

    def handle_admin_message(self, text: str):
        prompt_text = " ".join(text.split(" ")[1:])
        logger.info("handle_admin_message %s", prompt_text)
        create_prompt(self.db, prompt_text)
        self.send_prompts(prompt_text)

    def send_prompts(self, prompt_text: str):
        users = get_users(self.db, 0, 1000)
        logger.info("send_prompts %d %s", len(users), prompt_text)
        for user in users:
            self.send_prompt(user.phone, prompt_text)

    def send_prompt(self, phone: str, prompt_text: str):
        logger.info("send_prompt %s %s", phone, prompt_text)
        msg = PROMPT.format(prompt=prompt_text)
        self.send_message(phone, msg)

    def generate_url(self, user_hash: str):
        return BASE_URL + "v/" + user_hash
