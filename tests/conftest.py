import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔥 Force TEST database (SQLite, not Postgres)
TEST_DATABASE_URL = "sqlite:///./test.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.db.base import Base
from app.db.session import get_db
from app.db.init_db import init_roles
from app.main import app

from fastapi.testclient import TestClient


# Create SQLite engine for tests
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Create tables before tests start
Base.metadata.create_all(bind=engine)


# Seed roles before tests
def seed_roles():
    db = TestingSessionLocal()
    try:
        init_roles(db)
    finally:
        db.close()


seed_roles()


# Override DB dependency to use test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Provide test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
