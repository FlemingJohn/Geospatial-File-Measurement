from pathlib import Path

import geopandas

from app.readers.read_kml import read_kml
from app.readers.read_shapefile import read_shapefile


def read_file(path: Path) -> geopandas.GeoDataFrame:
    if path.suffix.lower() == ".zip":
        return read_shapefile(path)
    return read_kml(path)
