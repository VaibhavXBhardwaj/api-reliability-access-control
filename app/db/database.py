import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.environ["DATABASE_URL"]

MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )
        # Try connecting
        connection = engine.connect()
        connection.close()
        print("Database connected successfully.")
        break
    except OperationalError:
        print(f"Database not ready, retrying... ({attempt+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)
else:
    raise Exception("Could not connect to the database after multiple retries.")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
