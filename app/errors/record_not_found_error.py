from app.errors.api_error import ApiError


class RecordNotFoundError(ApiError):
    status_code = 404
    code = "file_not_found"
