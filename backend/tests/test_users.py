from models.user import User
from unittest.mock import MagicMock
from fastapi import HTTPException
from endpoints.user import (
    get_balance,
    get_current_user_info,
    get_users,
    read_user
)
import pytest


def make_user(id = 1, balance = 100.0):
    return User(
        id={id}, 
        name = f"User{id}",
        email=f"user{id}@example.com", 
        password = "hashedpassword",
        balance=balance)

def test_get_balance():
    user = make_user(balance=123.45)
    result = get_balance(current_user=user)
    assert result == {"balance": 123.45}

def test_get_current_user_info():
    user = make_user()
    result = get_current_user_info(current_user=user)
    assert result == user

def test_get_users_returns_all_users():
    users = [make_user(1), make_user(2)]

    mock_session = MagicMock()
    mock_session.exec.return_value.all.return_value = users

    current_user = make_user(id=99)

    result = get_users(session=mock_session, current_user=current_user)

    assert result == users
    mock_session.exec.assert_called_once()

def test_get_users_raises_http_exception_on_error():
    mock_session = MagicMock()
    mock_session.exec.side_effect = Exception("DB failure")

    current_user = make_user()

    with pytest.raises(HTTPException) as exc:
        get_users(session=mock_session, current_user=current_user)

    assert exc.value.status_code == 500
    assert "Error when fetching users" in exc.value.detail

def test_read_user_returns_user():
    user = make_user(id=42)

    mock_session = MagicMock()
    mock_session.get.return_value = user

    current_user = make_user(id=1)

    result = read_user(user_id=42, session=mock_session, current_user=current_user)

    assert result == user
    mock_session.get.assert_called_once_with(User, 42)

def test_read_user_not_found_raises_404():
    mock_session = MagicMock()
    mock_session.get.return_value = None

    current_user = make_user()

    with pytest.raises(HTTPException) as exc:
        read_user(user_id=999, session=mock_session, current_user=current_user)

    assert exc.value.status_code == 404
    assert "User not found" in exc.value.detail