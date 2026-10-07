from shapely.geometry import LineString, MultiLineString, MultiPolygon, box

from app.measurement.measure_geometry import measure_geometry


def test_polygon_gets_area_and_perimeter_only():
    result = measure_geometry(box(0, 0, 100, 100))
    assert result.area_square_meters == 10_000
    assert result.area_hectares == 1
    assert result.perimeter_meters == 400
    assert result.length_meters is None


def test_line_gets_length_only():
    result = measure_geometry(LineString([(0, 0), (300, 400)]))
    assert result.length_meters == 500
    assert result.area_square_meters is None
    assert result.perimeter_meters is None


def test_multipolygon_sums_its_parts():
    result = measure_geometry(MultiPolygon([box(0, 0, 100, 100), box(500, 500, 600, 600)]))
    assert result.area_square_meters == 20_000


def test_multilinestring_sums_its_parts():
    lines = MultiLineString([[(0, 0), (0, 100)], [(10, 10), (10, 60)]])
    assert measure_geometry(lines).length_meters == 150
