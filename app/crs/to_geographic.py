import geopandas

from app.settings.default_crs import DEFAULT_CRS


def to_geographic(features: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
    if features.crs is None:
        return features.set_crs(DEFAULT_CRS)
    return features.to_crs(DEFAULT_CRS)
