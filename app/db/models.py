from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    revoked = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)  # ✅ FIX ADDED
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
