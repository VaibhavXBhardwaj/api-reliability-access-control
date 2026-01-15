from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.auth.schemas import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse
)
from app.auth.service import create_user, authenticate_user
from app.core.jwt import create_access_token
from app.db.models import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=SignupResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(db, data.email, data.password)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token}

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
