from app.errors.api_error import ApiError


class FileTooLargeError(ApiError):
    status_code = 413
    code = "file_too_large"
