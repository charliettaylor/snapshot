from unittest.mock import MagicMock

from config import settings
from models import Registration
from text_test_client import TextTestClient

settings.twilio_account_sid = "please_dont_work"
settings.twilio_auth_token = "secret"
settings.twilio_phone_number = "8675309"


def test_handle_message_STOP_no_user():
    # Arrange
    db = MagicMock()

    crud = MagicMock()
    crud.get_reg = MagicMock(return_value=None)
    crud.create_reg = MagicMock(
        return_value=Registration(username="Jenny", phone="8675309", state=0)
    )
    crud.get_user_by_phone = MagicMock(return_value=None)

    ti = TextTestClient(db, settings, crud)
    # Act
    ti.handle_message("8675309", "STOP")

    # Assert
    crud.get_reg.assert_called_once_with(db, "8675309")
    crud.create_reg.assert_called_once_with(db, "8675309")


def test_handle_message_STOP_existing_user():
    # Arrange
    db = MagicMock()

    crud = MagicMock()
    crud.get_reg = MagicMock(
        return_value=Registration(username="Jenny", phone="8675309", state=0)
    )
    crud.create_reg = MagicMock(return_value=None)
    crud.get_user_by_phone = MagicMock(return_value=None)

    ti = TextTestClient(db, settings, crud)
    # Act
    ti.handle_message("8675309", "STOP")

    # Assert
    crud.get_reg.assert_called_once_with(db, "8675309")
    crud.create_reg.assert_not_called()
