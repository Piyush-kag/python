from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

from pydantic import ValidationError


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


async def custom_exception_handler(request: Request, exc: CustomException):
    logging.error(f"CustomException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"An unexpected error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": exc},
    )
