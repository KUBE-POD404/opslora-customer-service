from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.custom_exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    _ = request
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    _ = request
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    _ = request
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors()
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    _ = request
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error"
        }
    )