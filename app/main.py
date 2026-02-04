from fastapi import FastAPI

app = FastAPI(title="API Access Control")

@app.get("/health")
def health():
    return {"status": "ok"}

# Import router AFTER app creation
from app.api.v1.router import router as api_router
app.include_router(api_router, prefix="/v1")


@app.on_event("startup")
def startup():
    # Import DB stuff ONLY here
    from app.db.base import Base
    from app.db.database import engine
    from app.db.session import SessionLocal
    from app.db.init_db import init_roles

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        init_roles(db)
    finally:
        db.close()
