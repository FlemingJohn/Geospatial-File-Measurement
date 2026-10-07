from app.errors.unsupported_file_error import UnsupportedFileError
from app.settings.upload_limits import ALLOWED_EXTENSIONS


def validate_extension(extension: str) -> None:
    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        raise UnsupportedFileError(f"Unsupported file type '{extension}'. Upload one of: {allowed}")
