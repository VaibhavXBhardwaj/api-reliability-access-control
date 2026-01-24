from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.auth.router import router as auth_router
from app.auth.dependencies import get_current_user_optional

app = FastAPI(title="API Access Control")


# ---------- GLOBAL VALIDATION HANDLER ----------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


# ---------- AUTH CONTEXT MIDDLEWARE ----------

@app.middleware("http")
async def attach_user_to_request(request: Request, call_next):
    """
    Attach authenticated user (if any) to request.state
    so rate limiter and other middleware can access it.
    """
    request.state.user = None

    try:
        user = get_current_user_optional(request)
        request.state.user = user
    except Exception:
        # unauthenticated request → ignore
        pass

    response = await call_next(request)
    return response


# ---------- ROUTERS ----------

app.include_router(auth_router)


# ---------- HEALTH ----------

@app.get("/health")
def health():
    return {"status": "ok"}
