from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int):
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        print("✅ DECODED PAYLOAD:", payload)

        if payload.get("type") != "access":
            print("❌ WRONG TOKEN TYPE")
            return None

        return payload

    except JWTError as e:
        print("❌ JWT DECODE ERROR:", str(e))
        return None
