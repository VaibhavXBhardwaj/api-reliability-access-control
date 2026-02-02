from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.auth import schemas
from app.auth.service import create_user, authenticate_user, login_user
from app.auth.dependencies import require_role
from app.core.config import settings
from app.core.jwt import create_access_token, create_refresh_token
from app.core.rate_limit import rate_limit
from app.core.audit import log_action
from app.db.database import get_db
from app.db.models import User, RefreshToken

router = APIRouter(prefix="/auth", tags=["auth"])

# =========================
# SIGNUP
# =========================
@router.post(
    "/signup",
    response_model=schemas.SignupResponse,
    dependencies=[Depends(rate_limit("signup", 5, 60))]
)
def signup(
    request: Request,
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

    # 🔥 AUDIT LOG
    log_action(db, "user_signup", request, user.id)

    return user


# =========================
# LOGIN
# =========================
@router.post(
    "/login",
    response_model=schemas.LoginResponse,
    dependencies=[Depends(rate_limit("login", 5, 60))]
)
def login(
    request: Request,
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

    # 🔥 AUDIT LOG
    log_action(db, "login_success", request, user.id)

    return tokens


# =========================
# ADMIN-ONLY (RBAC CHECK)
# =========================
@router.get("/admin-only")
def admin_only_endpoint(
    admin: User = Depends(require_role("admin"))
):
    return {"message": "You are an admin. Authorization enforced."}


# =========================
# REFRESH TOKEN
# =========================
@router.post(
    "/refresh",
    response_model=schemas.TokenResponse,
    dependencies=[Depends(rate_limit("refresh", 10, 60))]
)
def refresh_access_token(
    request: Request,
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
        RefreshToken.revoked.is_(False)
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked"
        )

    db_token.revoked = True

    new_access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token({"sub": str(user_id)})

    db.add(
        RefreshToken(
            user_id=user_id,
            token=new_refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
    )

    db.commit()

    # 🔥 AUDIT LOG
    log_action(db, "token_refresh", request, user_id)

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
