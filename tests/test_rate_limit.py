from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limit import RATE_STORE

client = TestClient(app)


def test_rate_limit_triggers():
    # Reset limiter state before test
    RATE_STORE.clear()

    # Create a real user first
    client.post("/v1/auth/signup", json={
        "email": "ratelimit@example.com",
        "password": "StrongPass1"
    })

    # Spam login with WRONG password to trigger limiter
    last_response = None
    for _ in range(6):  # limit is 5 per minute
        last_response = client.post("/v1/auth/login", json={
            "email": "ratelimit@example.com",
            "password": "WrongPass1"
        })

    assert last_response.status_code == 429
    assert last_response.json()["detail"] == "Rate limit exceeded"
