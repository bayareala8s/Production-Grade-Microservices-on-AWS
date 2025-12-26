import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.routes import router as v1_router
from app.api.v2.routes import router as v2_router
from app.core.config import settings
from app.core.errors import ErrorBody, ErrorResponse
from app.core.logging import configure_logging
from app.core.middleware import RequestIdMiddleware
from app.health.routes import router as health_router


configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(RequestIdMiddleware)

app.include_router(health_router)
app.include_router(v1_router)
app.include_router(v2_router)


def _request_id(request: Request) -> str:
    rid = getattr(request.state, "request_id", None)
    return rid or "unknown"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorBody(
            code="validation_error",
            message="Request validation failed",
            details=exc.errors(),
        ),
        request_id=_request_id(request),
    )
    return JSONResponse(status_code=422, content=body.model_dump())


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = "not_found" if exc.status_code == 404 else "internal_error"
    msg = exc.detail if isinstance(exc.detail, str) else "Request failed"
    body = ErrorResponse(
        error=ErrorBody(code=code, message=msg, details=None),
        request_id=_request_id(request),
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled exception",
        extra={"extra": {"request_id": _request_id(request), "path": request.url.path}},
    )
    body = ErrorResponse(
        error=ErrorBody(code="internal_error", message="Internal server error", details=None),
        request_id=_request_id(request),
    )
    return JSONResponse(status_code=500, content=body.model_dump())


@app.get("/")
def root() -> dict[str, Any]:
    return {"service": settings.app_name, "env": settings.env}


