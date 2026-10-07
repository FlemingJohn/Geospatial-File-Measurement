import pytest
from shapely.geometry import GeometryCollection, LineString, MultiPoint, Point, Polygon, box

from app.measurement.get_measurement_status import get_measurement_status


@pytest.mark.parametrize(
    "geometry, expected",
    [
        (box(0, 0, 1, 1), "MEASURED"),
        (LineString([(0, 0), (1, 1)]), "MEASURED"),
        (Point(1, 1), "NOT_REQUIRED"),
        (MultiPoint([(0, 0), (1, 1)]), "NOT_REQUIRED"),
        (GeometryCollection([Point(1, 1), LineString([(0, 0), (1, 1)])]), "UNSUPPORTED"),
        (Polygon(), "UNSUPPORTED"),
        (None, "UNSUPPORTED"),
    ],
)
def test_status_matches_geometry_kind(geometry, expected):
    assert get_measurement_status(geometry) == expected
