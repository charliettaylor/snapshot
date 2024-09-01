from config import settings

PROD_ENV = "PROD"
BETA_ENV = "BETA"
DEV_ENV = "DEV"

BASE_URL = "https://snapshot.lieber.men/"
if settings.environment == BETA_ENV:
    BASE_URL = "https://dev.snapshot.lieber.men/"
if settings.environment == DEV_ENV:
    BASE_URL = "http://localhost:8000/"

NAME = "Snapshot"
EMOJI = "📸" if settings.environment == PROD_ENV else "📷"
SNAPSHOT = NAME + " " + EMOJI + ": "
SNAPSHOT_MULTI_LINE = NAME + " " + EMOJI

HOW_TO_START = SNAPSHOT + "Text START to play."
ENTER_USERNAME = SNAPSHOT + "Text STOP to unsubscribe.\n\nPlease enter your username:"
ENTER_USERNAME_AGAIN = SNAPSHOT + "please enter your username:"
CONFIRM_USERNAME = SNAPSHOT + 'You entered "{}", text YES to confirm or NO to change.'
BAD_USERNAME = (
    SNAPSHOT
    + "Username is invalid. Must be less than 16 characters and contain only letters, numbers, and underscores. Please try again:"
)
REGISTRATION_SUCCESSFUL = (
    SNAPSHOT + 'You\'ve successfully registered as "{}". Thanks! :)'
)
PROMPT = SNAPSHOT_MULTI_LINE + "\n\n✨{prompt}✨\n\nSTOP to unsubscribe."

START_KEYWORDS = ["START", "PLAY", "OPTIN", "SUBSCRIBE", "RESUBSCRIBE"]

POSITIVE_KEYWORDS = ["YES", "Y", "YE", "YEAH", "YEA", "CONFIRM", "YEP"]
NEGATIVE_KEYWORDS = ["NO", "N", "NOPE", "NAY", "NAH"]

INVALID_USER = SNAPSHOT + "Couldn't find user, please register first."
ALREADY_SUBMITTED = SNAPSHOT + "You already submitted for this prompt."
FAILED_PIC_SAVE = SNAPSHOT + "Couldn't save your pic, oops!"

VIEW_SUBMISSIONS = SNAPSHOT + "Thanks for submitting! View all submissions here:\n{}"
