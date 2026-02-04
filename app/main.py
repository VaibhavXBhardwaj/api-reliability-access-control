from fastapi import FastAPI

app = FastAPI(title="API Access Control")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():

    from app.db.database import engine
    from app.db.base import Base
    from app.db.session import SessionLocal
    from app.db.init_db import init_roles
    import app.db.models  # 👈 REGISTER ALL MODELS HERE

    # Create tables
   # Base.metadata.create_all(bind=engine)

    # Seed roles
    db = SessionLocal()
    try:
        init_roles(db)
    finally:
        db.close()


from app.api.v1.router import router as api_router
app.include_router(api_router, prefix="/v1")
