import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limit import RATE_STORE

client = TestClient(app)


def test_signup_and_login_flow():
    # 🔥 Reset rate limiter state before test
    RATE_STORE.clear()

    email = f"pytestuser_{uuid.uuid4()}@example.com"

    # ---------- SIGNUP ----------
    signup_response = client.post("/v1/auth/signup", json={
        "email": email,
        "password": "StrongPass1"
    })
    assert signup_response.status_code == 200
    data = signup_response.json()
    assert data["email"] == email
    assert "id" in data

    # ---------- LOGIN ----------
    login_response = client.post("/v1/auth/login", json={
        "email": email,
        "password": "StrongPass1"
    })
    assert login_response.status_code == 200
    tokens = login_response.json()

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

    # ---------- ACCESS PROTECTED ROUTE ----------
    protected = client.get(
        "/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )

    # Normal user should NOT be admin
    assert protected.status_code == 403
