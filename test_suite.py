from unittest.mock import MagicMock

from config import settings
from models import Registration
from TextTestClient import TextTestClient

settings.twilio_account_sid = "please_dont_work"
settings.twilio_auth_token = "secret"
settings.twilio_phone_number = "8675309"


USER = "Jenny"
NUM = "8675309"


def test_handle_message_no_reg():
    # Arrange
    db = MagicMock()

    db.get_reg = MagicMock(return_value=None)
    db.create_reg = MagicMock(
        return_value=Registration(username=USER, phone=NUM, state=0)
    )
    db.get_user_by_phone = MagicMock(return_value=None)

    tc = TextTestClient(settings, db)
    # Act
    tc.handle_message(NUM, "HI")

    # Assert
    db.get_reg.assert_called_once_with(NUM)
    db.create_reg.assert_called_once_with(NUM)


def test_handle_message_reg_state_0():
    # Arrange
    db = MagicMock()

    db.get_reg = MagicMock(return_value=Registration(username=USER, phone=NUM, state=0))
    db.create_reg = MagicMock(return_value=None)
    db.get_user_by_phone = MagicMock(return_value=None)

    tc = TextTestClient(settings, db)
    # Act
    tc.handle_message(NUM, "HI")

    # Assert
    db.get_reg.assert_called_once_with(NUM)
    db.create_reg.assert_not_called()


def test_handle_message_reg_state_1():
    # Arrange
    db = MagicMock()

    db.get_reg = MagicMock(return_value=Registration(username=USER, phone=NUM, state=1))
    db.create_reg = MagicMock(return_value=None)
    db.get_user_by_phone = MagicMock(return_value=None)
    db.update_reg = MagicMock(return_value=None)

    tc = TextTestClient(settings, db)
    # Act
    tc.handle_message(NUM, USER)

    # Assert
    db.get_reg.assert_called_once_with(NUM)
    # db.update_reg.assert_called_once()


def test_handle_message_reg_state_2():
    # Arrange
    db = MagicMock()

    db.get_reg = MagicMock(return_value=Registration(username=USER, phone=NUM, state=2))
    db.create_reg = MagicMock(return_value=None)
    db.get_user_by_phone = MagicMock(return_value=None)
    db.update_reg = MagicMock(return_value=None)
    db.create_user = MagicMock(return_value=None)
    db.get_current_prompt = MagicMock(return_value=None)

    tc = TextTestClient(settings, db)
    # Act
    tc.handle_message(NUM, "yes")

    # Assert
    db.get_reg.assert_called_once_with(NUM)
    db.create_user.assert_called_once_with(NUM, USER)
    db.update_reg.assert_called_once_with(NUM, 3, USER)
    db.get_current_prompt.assert_called_once()
