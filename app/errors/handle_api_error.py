from fastapi import Request
from fastapi.responses import JSONResponse

from app.errors.api_error import ApiError
from app.schemas.error_response import ErrorResponse


async def handle_api_error(request: Request, error: ApiError) -> JSONResponse:
    body = ErrorResponse(code=error.code, detail=error.detail)
    return JSONResponse(status_code=error.status_code, content=body.model_dump())
