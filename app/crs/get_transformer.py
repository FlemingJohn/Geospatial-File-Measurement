from functools import lru_cache

from pyproj import Transformer

from app.settings.default_crs import DEFAULT_CRS


@lru_cache(maxsize=128)
def get_transformer(epsg: int) -> Transformer:
    return Transformer.from_crs(DEFAULT_CRS, f"EPSG:{epsg}", always_xy=True)
