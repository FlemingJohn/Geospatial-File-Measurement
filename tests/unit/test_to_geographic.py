import pytest

from app.crs.get_crs_label import get_crs_label
from app.crs.get_crs_warnings import get_crs_warnings
from app.crs.to_geographic import to_geographic
from tests.builders.build_utm_square import build_utm_square


def test_projected_features_are_converted_to_degrees():
    converted = to_geographic(build_utm_square())
    longitude, latitude = converted.geometry.iloc[0].centroid.coords[0]
    assert longitude == pytest.approx(75.0, abs=0.01)
    assert latitude == pytest.approx(12.67, abs=0.05)


def test_missing_crs_is_assumed_to_be_wgs84_with_a_warning():
    features = build_utm_square().set_crs(None, allow_override=True)
    assert get_crs_label(features) == "EPSG:4326"
    assert len(get_crs_warnings(features)) == 1
    assert to_geographic(features).crs.to_epsg() == 4326


def test_known_crs_is_labelled_without_warnings():
    features = build_utm_square()
    assert get_crs_label(features) == "EPSG:32643"
    assert get_crs_warnings(features) == []
