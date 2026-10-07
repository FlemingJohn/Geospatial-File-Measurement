import geopandas

from app.settings.default_crs import DEFAULT_CRS


def get_crs_label(features: geopandas.GeoDataFrame) -> str:
    if features.crs is None:
        return DEFAULT_CRS
    authority = features.crs.to_authority()
    if authority:
        return f"{authority[0]}:{authority[1]}"
    return features.crs.name
