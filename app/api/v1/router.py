from fastapi import APIRouter
from app.auth.router import router as auth_router
from app.api.v1.audit import router as audit_router

router = APIRouter()

router.include_router(auth_router)

router.include_router(audit_router)
