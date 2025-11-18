import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from models.user import User
from models.transaction import Transaction
from endpoints.transaction import transfer_money


def create_user(id, balance):
    return User(id=id, name=f"User{id}", email=f"user{id}@example.com", password="hashed", balance=balance)


def test_transfer_money_success():
    sender = create_user(1, 100)
    receiver = create_user(2, 50)

    mock_db = MagicMock()
    mock_db.exec.side_effect = [
        MagicMock(one_or_none=lambda: sender),   
        MagicMock(one_or_none=lambda: receiver)  
    ]

    result = transfer_money(from_id=1, to_id=2, amount=30.0, db=mock_db)

    assert result["message"] == "Transaction succesful: 30.0 transferred from 1 to 2"
    assert sender.balance == 70.0
    assert receiver.balance == 80.0

    assert mock_db.add.call_count >= 3  # sender, receiver, transaction
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_any_call(sender)
    mock_db.refresh.assert_any_call(receiver)


def test_transfer_money_negative_amount():
    with pytest.raises(HTTPException) as exc:
        transfer_money(from_id=1, to_id=2, amount=0, db=MagicMock())

    assert exc.value.status_code == 400
    assert "greater than 0" in exc.value.detail


def test_transfer_money_sender_not_found():
    mock_db = MagicMock()
    mock_db.exec.side_effect = [
        MagicMock(one_or_none=lambda: None),  
        MagicMock(one_or_none=lambda: MagicMock()) #dummy receiver
    ]

    with pytest.raises(HTTPException) as exc:
        transfer_money(from_id=1, to_id=2, amount=50.0, db=mock_db)

    assert exc.value.status_code == 404
    assert "Sender not found" in exc.value.detail


def test_transfer_money_receiver_not_found():
    sender = create_user(1, 100)
    mock_db = MagicMock()
    mock_db.exec.side_effect = [
        MagicMock(one_or_none=lambda: sender),
        MagicMock(one_or_none=lambda: None)
    ]

    with pytest.raises(HTTPException) as exc:
        transfer_money(from_id=1, to_id=2, amount=50.0, db=mock_db)

    assert exc.value.status_code == 404
    assert "Receiver not found" in exc.value.detail


def test_transfer_money_insufficient_funds():
    sender = create_user(1, 20)
    receiver = create_user(2, 50)
    mock_db = MagicMock()
    mock_db.exec.side_effect = [
        MagicMock(one_or_none=lambda: sender),
        MagicMock(one_or_none=lambda: receiver)
    ]

    with pytest.raises(HTTPException) as exc:
        transfer_money(from_id=1, to_id=2, amount=30.0, db=mock_db)

    assert exc.value.status_code == 400
    assert "Insufficient balance" in exc.value.detail