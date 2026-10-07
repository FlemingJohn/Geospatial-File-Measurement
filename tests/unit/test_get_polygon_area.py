import pytest
from shapely.geometry import box

from app.measurement.get_polygon_area import get_polygon_area


def test_square_area_is_side_times_side():
    assert get_polygon_area(box(0, 0, 100, 100)) == 10_000


def test_hole_is_subtracted_from_area():
    with_hole = box(0, 0, 200, 200).difference(box(50, 50, 150, 150))
    assert get_polygon_area(with_hole) == pytest.approx(30_000)
