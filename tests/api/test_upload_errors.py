from zipfile import ZipFile

from tests.api.upload import upload
from tests.builders.build_kml_text import build_kml_text


def test_unsupported_extension_returns_415(client):
    response = upload(client, "notes.txt", "hello")
    assert response.status_code == 415
    assert response.json()["code"] == "unsupported_file_type"


def test_missing_file_returns_422(client):
    assert client.post("/api/files/").status_code == 422


def test_corrupt_kml_returns_400(client):
    response = upload(client, "broken.kml", "this is not xml")
    assert response.status_code == 400
    assert response.json()["code"] == "unreadable_file"


def test_kml_without_features_returns_422(client):
    response = upload(client, "empty.kml", build_kml_text(""))
    assert response.status_code == 422
    assert response.json()["code"] == "no_features_found"


def test_zip_that_is_not_an_archive_returns_400(client):
    response = upload(client, "fake.zip", "not a zip")
    assert response.status_code == 400
    assert response.json()["code"] == "invalid_zip"


def test_zip_without_shapefile_returns_400(client, tmp_path):
    archive_path = tmp_path / "empty.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("readme.txt", "no shapefile here")
    response = upload(client, "empty.zip", archive_path.read_bytes())
    assert response.status_code == 400
    assert response.json()["code"] == "missing_shapefile_parts"


def test_oversized_upload_returns_413(client, monkeypatch):
    monkeypatch.setattr("app.uploads.save_upload.MAXIMUM_UPLOAD_BYTES", 10)
    response = upload(client, "big.kml", "x" * 100)
    assert response.status_code == 413
    assert response.json()["code"] == "file_too_large"


def test_failed_upload_stores_nothing(client, tmp_path):
    upload(client, "broken.kml", "this is not xml")
    assert not (tmp_path / "storage").exists()
