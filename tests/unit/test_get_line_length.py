from shapely.geometry import LineString

from app.measurement.get_line_length import get_line_length


def test_line_length_follows_the_three_four_five_triangle():
    assert get_line_length(LineString([(0, 0), (300, 400)])) == 500


def test_zero_length_line_is_zero():
    assert get_line_length(LineString([(5, 5), (5, 5)])) == 0
