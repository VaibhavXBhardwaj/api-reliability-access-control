from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models import User, Role, RefreshToken
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token, create_refresh_token
from datetime import datetime


# -------------------------
# CREATE USER (SIGNUP)
# -------------------------
def create_user(db: Session, email: str, password: str) -> User:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # get default role = user
    role = db.query(Role).filter(Role.name == "user").first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role not found"
        )

    hashed_password = get_password_hash(password)

    user = User(
        email=email,
        password_hash=hashed_password,  # ✅ MATCHES DB COLUMN
        role_id=role.id                 # ✅ RBAC wired
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -------------------------
# AUTHENTICATE USER
# -------------------------
def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user


# -------------------------
# LOGIN USER
# -------------------------
def login_user(db: Session, user: User) -> dict:
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    refresh_entry = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        revoked=False,
        created_at=datetime.utcnow()
    )

    db.add(refresh_entry)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
