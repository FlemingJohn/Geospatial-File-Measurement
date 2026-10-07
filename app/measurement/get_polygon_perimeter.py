from shapely.geometry import Polygon


def get_polygon_perimeter(polygon: Polygon) -> float:
    return polygon.length
