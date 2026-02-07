from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.db.base import Base
from app.db.database import engine
from app.db.session import SessionLocal
from app.db.init_db import init_roles

app = FastAPI(title="API Access Control")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    # Create tables on startup
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        init_roles(db)
    finally:
        db.close()


# API routes
app.include_router(api_router, prefix="/v1")


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
