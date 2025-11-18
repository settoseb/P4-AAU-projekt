from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.base import create_db_and_tables
from endpoints import user, auth, transaction
from endpoints.auth import get_current_user
from db.session import get_db
from models.user import User
from sqlmodel import Session, select

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://bank.aau-projekt.dk",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(transaction.router, prefix="/transaction")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/saldo")
def homepage():
    return {"Saldo": 45.7}

# @app.get("/saldo")
# def homepage(
#    current_user: User = Depends(get_current_user),
#    db: Session = Depends(get_db)
# ):
#    user = db. exec(select(User).where(User.id == current_user.id)).one_or_none()
#    if not user:
#        raise HTTPException(status_code=404, detail="User not found")
#    return {"s#aldo": user.balance}
