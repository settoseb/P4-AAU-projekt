import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from main import app
from db.session import get_db

# Use in-memory SQLite for testing
test_engine = create_engine("sqlite:///:memory:", echo=False)

# Create DB and yield a session for each test
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

# Create a FastAPI test client that uses the test DB
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
