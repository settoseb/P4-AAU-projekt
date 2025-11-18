from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    amount: float = Field(default=None)
    from_id: int = Field(default=None, foreign_key="user.id")
    to_id: int = Field(default=None, foreign_key="user.id")
    balance_before: float = Field(default=None)
    balance_after: float = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionRequest(BaseModel):
    to_id: int
    amount: float


class TransactionResponse(BaseModel):
    id: int
    amount: float
    from_id: int
    to_id: int
    balance_before: float
    balance_after: float
    created_at: datetime

    class Config:
        orm_mode = True
