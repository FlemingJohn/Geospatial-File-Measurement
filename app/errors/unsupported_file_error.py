from app.errors.api_error import ApiError


class UnsupportedFileError(ApiError):
    status_code = 415
    code = "unsupported_file_type"
