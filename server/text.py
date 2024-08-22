from abc import ABC, abstractmethod


from util import super_good_hash
from schema import Registration, User
from database import get_db
from crud import *
from config import settings

BASE_URL = "https://snapshot.lieber.men/"

SNAPSHOT = "Snapshot 📸: "
SNAPSHOT_MULTI_LINE = "Snapshot 📸"

HOW_TO_START = SNAPSHOT + "Text START to play."
ENTER_USERNAME = (
    SNAPSHOT
    + "Text STOP to unsubscribe. To finish registering, please enter your username:"
)
ENTER_USERNAME_AGAIN = SNAPSHOT + "please enter your username:"
CONFIRM_USERNAME = SNAPSHOT + 'You entered "{}", text YES to confirm or NO to change.'
REGISTRATION_SUCCESSFUL = (
    SNAPSHOT + 'You\'ve successfully registered as "{}". Thanks! :)'
)
UNSUBSCRIBED = SNAPSHOT + "You've successfully unsubscribed. Text START to resubscribe."
PROMPT = SNAPSHOT_MULTI_LINE + "\n\n✨{prompt}✨\n\nSTOP to unsubscribe."

STOP_KEYWORDS = ["STOP", "UNSUBSCRIBE", "OPTOUT"]
START_KEYWORDS = ["START", "PLAY", "OPTIN", "SUBSCRIBE", "RESUBSCRIBE"]

POSITIVE_KEYWORDS = ["YES", "Y", "YE", "YEAH", "YEA", "CONFIRM", "YEP"]
NEGATIVE_KEYWORDS = ["NO", "N", "NOPE", "NAY", "NAH"]

INVALID_USER = SNAPSHOT + "Couldn't find user, please register first."
ALREADY_SUBMITTED = SNAPSHOT + "You already submitted for this prompt."
FAILED_PIC_SAVE = SNAPSHOT + "Couldn't save your pic, oops!"

VIEW_SUBMISSIONS = SNAPSHOT + "Thanks for submitting! View all submissions here:\n{}"


def contains(text: str, words: [str], ignore_case=True):
    for word in words:
        if word in text:
            return True
        if ignore_case and word.lower() in text.lower():
            return True
    return False


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

        if settings.admin_pass in text:
            self.handle_admin_message(text)

        reg = get_reg(self.db, from_)
        if reg is None:
            print("Creating registration...")
            reg = create_reg(self.db, from_)

        user = get_user_by_phone(self.db, from_)

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
            update_reg(self.db, Registration(phone=from_, username=None, state=1))
            self.send_message(from_, ENTER_USERNAME)

        elif reg.state == 0:
            self.send_message(from_, HOW_TO_START)

        elif reg.state == 1:
            update_reg(self.db, Registration(phone=from_, username=text, state=2))
            self.send_message(from_, CONFIRM_USERNAME.format(text))

        elif reg.state == 2 and contains(text, POSITIVE_KEYWORDS):
            user_hash = super_good_hash(reg.username)
            print(user_hash)
            create_user(
                self.db,
                User(
                    phone=from_,
                    username=reg.username,
                    active=True,
                    hash=super_good_hash(reg.username),
                    pics=None,
                ),
            )
            update_reg(
                self.db, Registration(phone=from_, username=reg.username, state=3)
            )
            self.send_message(from_, REGISTRATION_SUCCESSFUL.format(reg.username))

        elif reg.state == 2 and contains(text, NEGATIVE_KEYWORDS):
            update_reg(self.db, Registration(phone=from_, username=None, state=1))
            self.send_message(from_, ENTER_USERNAME_AGAIN)

    def handle_image(self, from_: str, url: str):
        user = get_user_by_phone(self.db, from_)

        if user is None:
            self.send_message(from_, INVALID_USER)
            return

        prompt = get_current_prompt(self.db)

        exists = get_submission_status(self.db, user.hash, prompt.id)

        if exists:
            self.send_message(from_, ALREADY_SUBMITTED)
            return

        pic = create_pic(
            self.db,
            schema.Pic(url=url, prompt=prompt, user=user.username),
        )

        if pic is None:
            self.send_message(from_, FAILED_PIC_SAVE)
        else:
            self.send_message(
                from_, VIEW_SUBMISSIONS.format(self.generate_url(user.hash))
            )

    def get_random_prompt(self):
        pass

    def handle_admin_message(self, text: str):
        prompt_text = " ".join(text.split(" ")[1:])
        create_prompt(self.db, prompt_text)
        self.send_prompts(prompt_text)

    def send_prompts(self, prompt: str):
        users = get_users(self.db, 0, 1000)
        for user in users:
            msg = PROMPT.format(prompt=prompt)
            self.send_message(user.phone, msg)

    def generate_url(self, user_hash: str):
        return BASE_URL + user_hash
