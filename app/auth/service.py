from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.models import User, RefreshToken, Role, AuditLog

from app.core.jwt import create_access_token, create_refresh_token
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- PASSWORD UTILS ----------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# ---------------- USER CREATION ----------------

def create_user(db: Session, email: str, password: str) -> User:
    user = User(
        email=email,
        password_hash=hash_password(password),
        role_id=1  # default role = user
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------- AUTHENTICATION ----------------

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def login_user(db, user):
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    db.add(
        RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }