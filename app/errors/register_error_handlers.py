from fastapi import FastAPI

from app.errors.api_error import ApiError
from app.errors.handle_api_error import handle_api_error


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, handle_api_error)
