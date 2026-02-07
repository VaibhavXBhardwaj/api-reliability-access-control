from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AuditLog
from app.auth.dependencies import require_role

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    admin = Depends(require_role("admin"))  # 🔥 only admin can view logs
):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()

    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "action": log.action,
            "endpoint": log.action,  # you don't store endpoint yet, so reuse action
        }
        for log in logs
    ]
