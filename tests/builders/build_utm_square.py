import geopandas
from shapely.geometry import box

UTM_ZONE_43_NORTH = "EPSG:32643"


def build_utm_square() -> geopandas.GeoDataFrame:
    square = box(500000, 1400000, 500100, 1400100)
    return geopandas.GeoDataFrame({"name": ["Parcel"]}, geometry=[square], crs=UTM_ZONE_43_NORTH)
