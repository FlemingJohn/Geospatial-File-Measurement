import json

from shapely.geometry.base import BaseGeometry
import shapely


def get_geometry_json(geometry: BaseGeometry | None) -> dict | None:
    if geometry is None:
        return None
    return json.loads(shapely.to_geojson(geometry))
