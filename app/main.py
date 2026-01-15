from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.auth.router import router as auth_router

app = FastAPI(title="API Access Control")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}
