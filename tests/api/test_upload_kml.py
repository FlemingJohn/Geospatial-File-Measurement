import pytest

from tests.api.upload import upload
from tests.builders.build_square_kml import build_square_kml


def test_upload_returns_file_information(client):
    response = upload(client, "survey.kml", build_square_kml())
    body = response.json()
    assert response.status_code == 201
    assert len(body["id"]) == 32
    assert body["filename"] == "survey.kml"
    assert body["feature_count"] == 1
    assert body["crs"] == "EPSG:4326"
    assert body["status"] == "COMPLETED"
    assert body["warnings"] == []


def test_polygon_is_measured_in_a_projected_crs(client):
    file_id = upload(client, "survey.kml", build_square_kml()).json()["id"]
    feature = client.get(f"/api/files/{file_id}/measurements/").json()["features"][0]
    assert feature["measurement_status"] == "MEASURED"
    assert feature["projected_crs"] == "EPSG:32631"
    assert feature["measurement"]["area_square_meters"] == pytest.approx(12_309, rel=0.01)
    assert feature["measurement"]["perimeter_meters"] == pytest.approx(443.8, rel=0.01)
    assert feature["measurement"]["length_meters"] is None
