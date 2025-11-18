from sqlmodel import SQLModel
from db.session import engine
from models.user import User
from models.transaction import Transaction

def delete_all_tables():
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("All tables have been dropped successfully!")

if __name__ == "__main__":
    delete_all_tables() 