from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.session import get_db
from typing import List, Optional
from models.transaction import Transaction, TransactionRequest, TransactionResponse
from models.user import User
from endpoints.auth import get_current_user


router = APIRouter()


def transfer_money(from_id: int, to_id: int, amount: float, db: Session):
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail="Amount must be greater than 0")

    try:
        sender_result = db.exec(select(User).where(User.id == from_id))
        sender = sender_result.one_or_none()

        receiver_result = db.exec(select(User).where(User.id == to_id))
        receiver = receiver_result.one_or_none()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver not found")
        if sender.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        balance_before = sender.balance
        sender.balance -= amount
        receiver.balance += amount
        balance_after = sender.balance

        db.add(sender)
        db.add(receiver)

        transaction = Transaction(
            from_id=sender.id,
            to_id=receiver.id,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after
        )
        print(transaction)
        db.add(transaction)
        db.commit()
        db.refresh(sender)
        db.refresh(receiver)
        db.refresh(transaction)
        return {"message": f"Transaction succesful: {amount} transferred from {from_id} to {to_id}"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Transaction failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Transaction failed: {str(e)}")


@router.post("/transaction", tags=["Transactions"])
def transaction(data: TransactionRequest,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_db)):
    return transfer_money(current_user.id, data.to_id, data.amount, session)


@router.get("/transactions", response_model=List[TransactionResponse])
def get_user_transactions(

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        transactions = db.exec(
            select(Transaction).where(
                (Transaction.from_id == current_user.id) | (
                    Transaction.to_id == current_user.id)
            )
        ).all()

        if not transactions:
            return {"message": "No transactions found for the current user"}

        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error fetching transactions")
