from pathlib import Path
from zipfile import BadZipFile, ZipFile

from app.errors.invalid_zip_error import InvalidZipError
from app.readers.check_archive_size import check_archive_size
from app.readers.check_member_paths import check_member_paths


def extract_zip(zip_path: Path, destination: Path) -> None:
    try:
        with ZipFile(zip_path) as archive:
            check_archive_size(archive)
            check_member_paths(archive, destination)
            archive.extractall(destination)
    except BadZipFile as error:
        raise InvalidZipError("The uploaded file is not a valid zip archive") from error
