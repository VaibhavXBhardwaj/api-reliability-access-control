from sqlalchemy.orm import Session
from fastapi import Request
from app.db.models import AuditLog


def log_action(
    db: Session,
    action: str,
    request: Request,
    user_id: int | None = None,
):
    log = AuditLog(
        action=action,
        user_id=user_id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    db.commit()
