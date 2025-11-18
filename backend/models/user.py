from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import constr
from datetime import datetime

class UserBase(SQLModel):
    name: str = Field(default=None, nullable=False)
    email: str = Field(default=None, nullable=False, unique=True)

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(default=None, nullable=False)
    is_admin: bool = Field(default=False)
    balance: float = Field(default=100.0)
    verification_code: Optional[str] = Field(default=None)
    verification_code_expires: Optional[datetime] = Field(default=None)

class UserResponse(UserBase):
    balance: float

class UserLogin(SQLModel):
    email: str
    password: str