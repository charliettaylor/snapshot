BASE_URL = "https://snapshot.lieber.men/"

SNAPSHOT = "Snapshot 📸: "
SNAPSHOT_MULTI_LINE = "Snapshot 📸"

HOW_TO_START = SNAPSHOT + "Text START to play."
ENTER_USERNAME = (
    SNAPSHOT_MULTI_LINE
    + "\nText STOP to unsubscribe.\n\n To finish registering, please enter your username:"
)
ENTER_USERNAME_AGAIN = SNAPSHOT + "please enter your username:"
CONFIRM_USERNAME = SNAPSHOT + 'You entered "{}", text YES to confirm or NO to change.'
BAD_USERNAME = (
    SNAPSHOT
    + "Username is invalid. Must be less than 16 characters and contain only letters, numbers, and underscores. Please try again:"
)
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
