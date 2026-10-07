from shapely.geometry.base import BaseGeometry


def select_parts(parts: list[BaseGeometry], geometry_type: str) -> list[BaseGeometry]:
    return [part for part in parts if part.geom_type == geometry_type]
