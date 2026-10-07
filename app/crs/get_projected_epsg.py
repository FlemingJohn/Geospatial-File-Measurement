from shapely.geometry.base import BaseGeometry

NORTH_POLAR_LIMIT = 84
SOUTH_POLAR_LIMIT = -80
NORTH_POLAR_EPSG = 32661
SOUTH_POLAR_EPSG = 32761
NORTH_UTM_BASE = 32600
SOUTH_UTM_BASE = 32700


def get_projected_epsg(geometry: BaseGeometry) -> int:
    centroid = geometry.centroid
    if centroid.y > NORTH_POLAR_LIMIT:
        return NORTH_POLAR_EPSG
    if centroid.y < SOUTH_POLAR_LIMIT:
        return SOUTH_POLAR_EPSG
    zone = min(int((centroid.x + 180) // 6) + 1, 60)
    return (NORTH_UTM_BASE if centroid.y >= 0 else SOUTH_UTM_BASE) + zone
