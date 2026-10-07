from app.errors.api_error import ApiError


class InvalidZipError(ApiError):
    status_code = 400
    code = "invalid_zip"
