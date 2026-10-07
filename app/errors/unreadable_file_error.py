from app.errors.api_error import ApiError


class UnreadableFileError(ApiError):
    status_code = 400
    code = "unreadable_file"
