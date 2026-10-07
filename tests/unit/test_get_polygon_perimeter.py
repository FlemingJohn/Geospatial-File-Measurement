from shapely.geometry import box

from app.measurement.get_polygon_perimeter import get_polygon_perimeter


def test_square_perimeter_is_four_sides():
    assert get_polygon_perimeter(box(0, 0, 100, 100)) == 400
