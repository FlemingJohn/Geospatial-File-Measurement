from zipfile import ZipFile

import pytest

from app.errors.invalid_zip_error import InvalidZipError
from app.readers.extract_zip import extract_zip


def test_unsafe_member_path_is_rejected(tmp_path):
    archive_path = tmp_path / "unsafe.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("../escaped.txt", "data")
    with pytest.raises(InvalidZipError):
        extract_zip(archive_path, tmp_path / "output")


def test_file_that_is_not_a_zip_is_rejected(tmp_path):
    fake = tmp_path / "fake.zip"
    fake.write_text("not a zip")
    with pytest.raises(InvalidZipError):
        extract_zip(fake, tmp_path / "output")


def test_valid_zip_is_extracted(tmp_path):
    archive_path = tmp_path / "valid.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("inside.txt", "data")
    destination = tmp_path / "output"
    destination.mkdir()
    extract_zip(archive_path, destination)
    assert (destination / "inside.txt").read_text() == "data"
