from shapely.geometry.base import BaseGeometry


def split_geometry_parts(geometry: BaseGeometry) -> list[BaseGeometry]:
    if hasattr(geometry, "geoms"):
        return [part for child in geometry.geoms for part in split_geometry_parts(child)]
    return [geometry]
