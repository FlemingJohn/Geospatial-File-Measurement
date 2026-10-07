from shapely.geometry.base import BaseGeometry

from app.schemas.measurement_status import MeasurementStatus

MEASURED_TYPES = {"Polygon", "MultiPolygon", "LineString", "MultiLineString"}
NOT_REQUIRED_TYPES = {"Point", "MultiPoint"}


def get_measurement_status(geometry: BaseGeometry | None) -> MeasurementStatus:
    if geometry is None or geometry.is_empty:
        return "UNSUPPORTED"
    if geometry.geom_type in MEASURED_TYPES:
        return "MEASURED"
    if geometry.geom_type in NOT_REQUIRED_TYPES:
        return "NOT_REQUIRED"
    return "UNSUPPORTED"
