import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limit import RATE_STORE

client = TestClient(app)


def test_admin_endpoint_denied_for_normal_user():
    # 🔥 Reset rate limiter so previous tests don’t affect this one
    RATE_STORE.clear()

    email = f"rbacuser_{uuid.uuid4()}@example.com"

    # ---------- CREATE NORMAL USER ----------
    signup = client.post("/v1/auth/signup", json={
        "email": email,
        "password": "StrongPass1"
    })
    assert signup.status_code == 200

    # ---------- LOGIN ----------
    login = client.post("/v1/auth/login", json={
        "email": email,
        "password": "StrongPass1"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]

    # ---------- TRY ADMIN ENDPOINT ----------
    response = client.get(
        "/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should be forbidden (RBAC working)
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
