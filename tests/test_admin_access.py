import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.session import SessionLocal
from app.db.models import User, Role
from app.core.rate_limit import RATE_STORE

client = TestClient(app)


def promote_user_to_admin(email: str):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == email).first()
    admin_role = db.query(Role).filter(Role.name == "admin").first()

    user.role_id = admin_role.id
    db.commit()
    db.close()


def test_admin_access_control():
    RATE_STORE.clear()

    # -------- CREATE NORMAL USER --------
    email = f"admin_test_{uuid.uuid4()}@example.com"

    signup = client.post("/v1/auth/signup", json={
        "email": email,
        "password": "StrongPass1"
    })
    assert signup.status_code == 200

    login = client.post("/v1/auth/login", json={
        "email": email,
        "password": "StrongPass1"
    })
    token = login.json()["access_token"]

    # -------- NORMAL USER SHOULD FAIL --------
    res = client.get(
        "/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403

    # -------- PROMOTE TO ADMIN --------
    promote_user_to_admin(email)

    # Need fresh login to reflect role change in token
    login = client.post("/v1/auth/login", json={
        "email": email,
        "password": "StrongPass1"
    })
    admin_token = login.json()["access_token"]

    # -------- ADMIN SHOULD SUCCEED --------
    res = client.get(
        "/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["message"] == "You are an admin. Authorization enforced."
