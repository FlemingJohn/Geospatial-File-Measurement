from shapely.geometry.base import BaseGeometry

from app.measurement.get_line_length import get_line_length
from app.measurement.get_polygon_area import get_polygon_area
from app.measurement.get_polygon_perimeter import get_polygon_perimeter
from app.measurement.select_parts import select_parts
from app.measurement.split_geometry_parts import split_geometry_parts
from app.measurement.sum_measurements import sum_measurements
from app.schemas.feature_measurement import FeatureMeasurement

SQUARE_METERS_PER_HECTARE = 10_000


def measure_geometry(projected_geometry: BaseGeometry) -> FeatureMeasurement:
    parts = split_geometry_parts(projected_geometry)
    polygons = select_parts(parts, "Polygon")
    lines = select_parts(parts, "LineString")
    area = sum_measurements(polygons, get_polygon_area)
    return FeatureMeasurement(
        area_square_meters=area,
        area_hectares=None if area is None else round(area / SQUARE_METERS_PER_HECTARE, 6),
        perimeter_meters=sum_measurements(polygons, get_polygon_perimeter),
        length_meters=sum_measurements(lines, get_line_length),
    )
