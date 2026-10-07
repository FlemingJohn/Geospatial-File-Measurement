from app.errors.api_error import ApiError


class EmptyFileError(ApiError):
    status_code = 422
    code = "no_features_found"
