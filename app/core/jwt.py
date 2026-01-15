from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
