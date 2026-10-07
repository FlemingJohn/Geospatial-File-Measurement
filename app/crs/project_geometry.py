from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from app.crs.get_transformer import get_transformer


def project_geometry(geometry: BaseGeometry, epsg: int) -> BaseGeometry:
    return transform(get_transformer(epsg).transform, geometry)
