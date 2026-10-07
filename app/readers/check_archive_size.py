from zipfile import ZipFile

from app.errors.file_too_large_error import FileTooLargeError
from app.settings.upload_limits import MAXIMUM_EXTRACTED_BYTES


def check_archive_size(archive: ZipFile) -> None:
    extracted_bytes = sum(member.file_size for member in archive.infolist())
    if extracted_bytes > MAXIMUM_EXTRACTED_BYTES:
        raise FileTooLargeError("The zip archive expands to more than the allowed size")
