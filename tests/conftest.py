import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db import models  # ensures models are registered
from app.db.init_db import init_roles  # 🔥 IMPORT ROLE SEEDER

TEST_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed default roles (user, admin, etc.)
    db = TestingSessionLocal()
    try:
        init_roles(db)   # 🔥 THIS FIXES YOUR ERROR
    finally:
        db.close()

    yield

    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)
