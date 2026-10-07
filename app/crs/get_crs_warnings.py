import geopandas

from app.settings.default_crs import DEFAULT_CRS


def get_crs_warnings(features: geopandas.GeoDataFrame) -> list[str]:
    if features.crs is None:
        return [f"No coordinate reference system was found in the file, so {DEFAULT_CRS} was assumed"]
    return []
