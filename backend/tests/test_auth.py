from datetime import datetime, timedelta
import pytest
from unittest.mock import MagicMock, patch
from endpoints.auth import login, signup, two_factor_validation
from models.user import User, UserCreate, UserLogin
   

def test_signup():
    user_create = UserCreate(email="user1@example.com", name="user1", password="pasword123!")
    

    mock_session = MagicMock()
    mock_session.exec.return_value.first.return_value = None

    with patch("endpoints.auth.is_password_leaked", return_value=False), \
         patch("endpoints.auth.pwd_context.hash", return_value="hashedpassword"):
        mock_user = signup(user_create=user_create, session=mock_session)

    assert mock_user.email == "user1@example.com"
    mock_session.add.assert_called_once
    mock_session.commit.assert_called_once
    mock_session.refresh.assert_called_once

def test_login():
    user_login = UserLogin(email="user2@example.com", name="user2", password="pasword123!")
    user = User(email="user2@example.com", password = "hashedpass")

    mock_session = MagicMock()
    mock_session.exec.return_value.first.return_value = user

    with patch("endpoints.auth.pwd_context.verify", return_value=True), \
         patch("endpoints.auth.send_2fa_email", return_value=None):
        response = login(user_login=user_login, session=mock_session)

    assert "Verification code is send" in response["message"]
    assert user.verification_code is not None
    assert user.verification_code_expires is not None
    assert mock_session.commit.called

def test_two_factor_validation():
    mock_session=MagicMock()
    user = User(
        email = "user2@example.com",
        verification_code= "123456",
        verification_code_expires = datetime.utcnow() + timedelta(minutes=5)
    )

    mock_session.exec.return_value.first.return_value = user

    with patch("endpoints.auth.create_access_token", return_value="mock.jwt.token"):
        result = two_factor_validation(verification_code="123456", email="user2@example.com", session=mock_session)

    assert result["access_token"] == "mock.jwt.token"
    assert user.verification_code is None
    assert mock_session.commit.called