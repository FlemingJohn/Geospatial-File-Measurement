from pathlib import Path
from zipfile import ZipFile

from app.errors.invalid_zip_error import InvalidZipError


def check_member_paths(archive: ZipFile, destination: Path) -> None:
    root = destination.resolve()
    for name in archive.namelist():
        if not (root / name).resolve().is_relative_to(root):
            raise InvalidZipError(f"The zip archive contains an unsafe path: {name}")
