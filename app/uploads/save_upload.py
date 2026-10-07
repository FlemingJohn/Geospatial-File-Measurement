from pathlib import Path
from typing import BinaryIO

from app.errors.file_too_large_error import FileTooLargeError
from app.settings.upload_limits import CHUNK_BYTES, MAXIMUM_UPLOAD_BYTES


def save_upload(source: BinaryIO, destination: Path) -> Path:
    total_bytes = 0
    with destination.open("wb") as target:
        while chunk := source.read(CHUNK_BYTES):
            total_bytes += len(chunk)
            check_size(total_bytes)
            target.write(chunk)
    return destination


def check_size(total_bytes: int) -> None:
    if total_bytes > MAXIMUM_UPLOAD_BYTES:
        limit_megabytes = MAXIMUM_UPLOAD_BYTES // (1024 * 1024)
        raise FileTooLargeError(f"File is larger than the {limit_megabytes} MB limit")
