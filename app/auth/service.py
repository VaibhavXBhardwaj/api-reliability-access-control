from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.models import User, RefreshToken
from app.core.security import verify_password, get_password_hash
from app.core.jwt import create_access_token, create_refresh_token


# ---------- SIGNUP ----------

def create_user(db: Session, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)

    user = User(
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ---------- LOGIN ----------

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, user: User):
    # create access token (short lived)
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    # create refresh token (long lived)
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    # store refresh token in DB (stateful control)
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
