import pytest

from tests.api.upload import upload
from tests.builders.build_mixed_kml import build_mixed_kml


def get_features(client):
    file_id = upload(client, "mixed.kml", build_mixed_kml()).json()["id"]
    response = client.get(f"/api/files/{file_id}/measurements/")
    assert response.status_code == 200
    return response.json()["features"]


def test_every_feature_has_the_required_fields(client):
    for feature in get_features(client)[:4]:
        assert set(feature) >= {"id", "geometry_type", "geometry", "crs", "properties"}
        assert feature["crs"] == "EPSG:4326"


def test_features_are_numbered_from_one(client):
    assert [feature["id"] for feature in get_features(client)] == [1, 2, 3, 4, 5]


def test_properties_and_geometry_are_returned(client):
    polygon = get_features(client)[0]
    assert polygon["properties"]["Name"] == "Square"
    assert polygon["geometry_type"] == "Polygon"
    assert polygon["geometry"]["type"] == "Polygon"


def test_line_is_measured_for_length(client):
    line = get_features(client)[1]
    assert line["measurement_status"] == "MEASURED"
    assert line["measurement"]["length_meters"] == pytest.approx(1113.19, rel=0.005)


def test_point_needs_no_measurement(client):
    point = get_features(client)[2]
    assert point["measurement_status"] == "NOT_REQUIRED"
    assert point["measurement"] is None
    assert point["projected_crs"] is None


def test_mixed_collection_is_unsupported_instead_of_failing(client):
    collection = get_features(client)[3]
    assert collection["geometry_type"] == "GeometryCollection"
    assert collection["measurement_status"] == "UNSUPPORTED"
    assert collection["measurement"] is None


def test_feature_without_geometry_is_unsupported(client):
    empty = get_features(client)[4]
    assert empty["geometry"] is None
    assert empty["geometry_type"] is None
    assert empty["measurement_status"] == "UNSUPPORTED"


def test_totals_count_features_and_sum_measurements(client):
    file_id = upload(client, "mixed.kml", build_mixed_kml()).json()["id"]
    totals = client.get(f"/api/files/{file_id}/measurements/").json()["totals"]
    assert totals["feature_count"] == 5
    assert totals["measured_feature_count"] == 2
    assert totals["unsupported_feature_count"] == 2
    assert totals["total_length_meters"] == pytest.approx(1113.19, rel=0.005)
