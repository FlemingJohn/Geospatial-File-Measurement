import pytest

from tests.builders.build_shapefile_zip import build_shapefile_zip
from tests.builders.build_utm_square import build_utm_square


def upload_archive(client, archive):
    return client.post("/api/files/", files={"file": ("parcels.zip", archive.read_bytes())})


def get_feature(client, file_id):
    return client.get(f"/api/files/{file_id}/measurements/").json()["features"][0]


def test_projected_shapefile_keeps_its_crs_and_is_measured_in_square_meters(client, tmp_path):
    uploaded = upload_archive(client, build_shapefile_zip(build_utm_square(), tmp_path)).json()
    feature = get_feature(client, uploaded["id"])
    assert uploaded["crs"] == "EPSG:32643"
    assert feature["crs"] == "EPSG:32643"
    assert feature["properties"] == {"name": "Parcel"}
    assert feature["projected_crs"] == "EPSG:32643"
    assert feature["measurement"]["area_square_meters"] == pytest.approx(10_000, rel=0.001)
    assert feature["measurement"]["perimeter_meters"] == pytest.approx(400, rel=0.001)


def test_geometry_is_returned_in_the_file_crs(client, tmp_path):
    uploaded = upload_archive(client, build_shapefile_zip(build_utm_square(), tmp_path)).json()
    ring = get_feature(client, uploaded["id"])["geometry"]["coordinates"][0]
    assert sorted({corner[0] for corner in ring}) == [500_000, 500_100]
    assert sorted({corner[1] for corner in ring}) == [1_400_000, 1_400_100]


def test_shapefile_without_projection_file_warns_and_assumes_wgs84(client, tmp_path):
    archive = build_shapefile_zip(build_utm_square().set_crs(None, allow_override=True), tmp_path)
    body = upload_archive(client, archive).json()
    assert body["crs"] == "EPSG:4326"
    assert len(body["warnings"]) == 1
