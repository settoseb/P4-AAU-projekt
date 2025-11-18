from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from models.user import User, UserCreate, UserResponse, UserLogin
from db.session import get_db
from passlib.context import CryptContext
from passlib.hash import argon2
from datetime import datetime, timedelta
import jwt
from config import settings
import random

from utils.email import send_2fa_email
from utils.haveibeenpwned import is_password_leaked

router = APIRouter()
pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__type="ID",        # Use Argon2id variant
    argon2__time_cost=2,      # 2 iterations
    argon2__memory_cost=47104,  # 46 MB
    argon2__parallelism=1     # 1 degree of parallelism
)
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = session.exec(select(User).where(User.email == user_email)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/login", tags=["Authentication"])
def login(user_login: UserLogin, session: Session = Depends(get_db)):
    """
    Authenticate user
    """
    statement = select(User).where(User.email == user_login.email)
    user = session.exec(statement).first()

    if not user or not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    verification_code = str(random.randint(000000, 999999)).zfill(6)
    verification_code_expiration = datetime.utcnow() + timedelta(minutes=5)
    user.verification_code = verification_code
    user.verification_code_expires = verification_code_expiration
    session.commit()

    send_2fa_email(user.email, verification_code)

    return {"message": "Verification code is send to your email"}


@router.post("/verify", tags=["Authentication"])
def two_factor_validation(verification_code: str, email: str, session: Session = Depends(get_db)):

    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or user.verification_code != verification_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect code"
        )

    if user.verification_code_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Code has expired"
        )

    user.verification_code = None
    user.verification_code_expires = None
    session.commit()

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserResponse, tags=["Authentication"])
def signup(user_create: UserCreate, session: Session = Depends(get_db)) -> UserResponse:
    """
    Create a new user and add it to the database.
    """
    try:
        statement = select(User).where(User.email == user_create.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        if is_password_leaked(user_create.password):
            raise HTTPException(
                status_code=400,
                detail="Your password is found in a public data breach. Please use another one"
            )

        user = User(
            email=user_create.email,
            name=user_create.name,
            password=pwd_context.hash(user_create.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error creating user: {str(e)}")
