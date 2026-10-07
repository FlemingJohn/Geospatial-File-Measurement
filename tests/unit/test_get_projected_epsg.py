import pytest
from shapely.geometry import Point

from app.crs.get_projected_epsg import get_projected_epsg


@pytest.mark.parametrize(
    "longitude, latitude, expected",
    [
        (77.59, 12.97, 32643),
        (-0.12, 51.5, 32630),
        (151.2, -33.9, 32756),
        (179.9, 10, 32660),
        (0, 89, 32661),
        (0, -85, 32761),
    ],
)
def test_zone_comes_from_the_feature_location(longitude, latitude, expected):
    assert get_projected_epsg(Point(longitude, latitude)) == expected
