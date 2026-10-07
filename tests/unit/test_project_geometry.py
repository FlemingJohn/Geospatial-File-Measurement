import pytest
from shapely.geometry import Point

from app.crs.project_geometry import project_geometry


def test_point_on_the_central_meridian_lands_on_the_false_easting():
    projected = project_geometry(Point(75.0, 0.0), 32643)
    assert projected.x == pytest.approx(500_000, abs=0.01)
    assert projected.y == pytest.approx(0, abs=0.01)


def test_one_degree_of_latitude_is_about_111_kilometers_after_projection():
    start = project_geometry(Point(75.0, 10.0), 32643)
    end = project_geometry(Point(75.0, 11.0), 32643)
    assert end.y - start.y == pytest.approx(110_600, rel=0.01)
