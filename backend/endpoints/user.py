from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models.user import User, UserResponse
from db.session import get_db
from endpoints.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse, tags=["Users"])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's information.
    Requires authentication via JWT token.
    """
    return current_user


@router.get("/balance")
def get_balance(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's balance.
    Requires authentication via JWT token.
    """
    return {"balance": current_user.balance}


@router.get("/", response_model=List[UserResponse], tags=["Users"])
def get_users(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all users from database.
    """
    try:
        statement = select(User)
        users = session.exec(statement).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error when fetching users: {str(e)}")


@router.get("/{user_id}", response_model=User, tags=["Users"])
def read_user(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found.")
    return user


@router.patch("/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, new_user: User, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    with Session(get_db()) as session:
        user_from_db = session.get(User, user_id)
        if not user_from_db:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user_info = new_user.model.dump(exclude_unset=True)
        user_from_db.sqlmodel_update(updated_user_info)

        session.add(user_from_db)
        session.commit()
        session.refresh(user_from_db)
        return user_from_db
