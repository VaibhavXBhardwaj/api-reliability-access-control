from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.auth.router import router as auth_router

app = FastAPI(title="API Access Control Service", version="1.0.0")


# ---------- GLOBAL VALIDATION ERROR FORMAT ----------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []

    for err in exc.errors():
        formatted_errors.append({
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={"errors": formatted_errors}
    )


# ---------- ROUTERS ----------
app.include_router(auth_router, prefix="/v1")


# ---------- HEALTH CHECK ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}
