import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models.base import User, Company, Task
from passlib.context import CryptContext

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(autouse=True,scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_company(setup_database):
    db = TestingSessionLocal()
    company = Company(
        name="Test Company",
        description="Test",
        mode="public",
        rating=5
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    db.close()
    return company

@pytest.fixture
def test_user(setup_database, test_company):
    db = TestingSessionLocal()
    hashed_pw = pwd_context.hash("testpass")
    user = User(
        username="testuser",
        email="test@example.com",
        password=hashed_pw,
        first_name="Test",
        last_name="User",
        is_active=True,
        is_admin=False,
        company_id=test_company.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture
def test_task(setup_database, test_user):
    db = TestingSessionLocal()
    task = Task(
        summary="Test Task",
        description="Task description",
        status=True,
        priority=3,
        user_id=test_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return task