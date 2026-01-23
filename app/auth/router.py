from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.auth import schemas
from app.auth.service import create_user, authenticate_user, login_user
from app.core.config import settings
from app.core.jwt import create_access_token, create_refresh_token
from app.db.database import get_db
from app.db.models import User, RefreshToken
from app.auth.dependencies import require_role

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------- SIGNUP ----------

@router.post("/signup", response_model=schemas.SignupResponse)
def signup(
    data: schemas.SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = create_user(db, data.email, data.password)
    return user


# ---------- LOGIN ----------

@router.post("/login", response_model=schemas.LoginResponse)
def login(
    data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    tokens = login_user(db, user)
    return tokens

@router.get("/admin-only")
def admin_only_endpoint(
    admin = Depends(require_role("admin"))
):
    return {
        "message": "You are an admin. Authorization enforced."
    }

# ---------- REFRESH ----------

@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_access_token(
    data: schemas.RefreshRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = int(payload.get("sub"))

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == data.refresh_token,
        RefreshToken.revoked == False
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked"
        )

    # 🔥 revoke old refresh token
    db_token.revoked = True

    # issue new tokens
    new_access_token = create_access_token(
        data={"sub": str(user_id)}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": str(user_id)}
    )

    db.add(
        RefreshToken(
            user_id=user_id,
            token=new_refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
    )

    db.commit()

    return {
        "access_token": new_access_token
    }
