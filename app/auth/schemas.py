from pydantic import BaseModel, EmailStr


# ---------- SIGNUP ----------

class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    id: int
    email: EmailStr


# ---------- LOGIN ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ---------- REFRESH ----------

class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
