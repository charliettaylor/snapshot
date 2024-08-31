import re
from unittest.mock import MagicMock

from config import settings
from models import Registration
from TestClient import TestClient

settings.twilio_account_sid = "please_dont_work"
settings.twilio_auth_token = "secret"
settings.twilio_phone_number = "8675309"


def test_handle_message_no_reg():
    # Arrange
    db = MagicMock()

    db.get_reg = MagicMock(return_value=None)
    # db.create_reg = MagicMock(
    #     return_value=Registration(username="Jenny", phone="8675309", state=0)
    # )
    db.get_user_by_phone = MagicMock(return_value=None)

    tc = TestClient(settings, db)
    # Act
    tc.receive_message("8675309", "HI")

    # Assert
    db.get_reg.assert_called_once_with("8675309")
    db.create_reg.assert_called_once_with("8675309")
