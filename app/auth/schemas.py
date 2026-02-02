from pydantic import BaseModel, EmailStr, Field, field_validator


# =========================
# SIGNUP
# =========================

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        example="StrongPass123"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str):
        if v.islower() or v.isupper() or v.isalpha() or v.isdigit():
            raise ValueError(
                "Password must include a mix of upper/lowercase letters and numbers"
            )
        return v


class SignupResponse(BaseModel):
    id: int
    email: EmailStr


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# =========================
# REFRESH TOKEN
# =========================

class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
