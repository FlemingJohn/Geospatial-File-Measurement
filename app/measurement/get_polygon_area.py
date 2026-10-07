from shapely.geometry import Polygon


def get_polygon_area(polygon: Polygon) -> float:
    return polygon.area
