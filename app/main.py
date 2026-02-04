from fastapi import FastAPI
from app.api.v1.router import router as api_router
from app.db.base import Base
from app.db.database import engine
from app.db.session import SessionLocal
from app.db.init_db import init_roles
from app.db import models  # register models

app = FastAPI(title="API Access Control")


@app.on_event("startup")
def startup():
    # Create tables AFTER app starts (not at import time)
    Base.metadata.create_all(bind=engine)

    # Seed roles
    db = SessionLocal()
    try:
        init_roles(db)
    finally:
        db.close()


app.include_router(api_router, prefix="/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
