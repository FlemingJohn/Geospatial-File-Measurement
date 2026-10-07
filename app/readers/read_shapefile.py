from pathlib import Path
from tempfile import TemporaryDirectory

import geopandas

from app.readers.check_shapefile_parts import check_shapefile_parts
from app.readers.extract_zip import extract_zip
from app.readers.find_shapefile import find_shapefile
from app.readers.read_layer import read_layer


def read_shapefile(zip_path: Path) -> geopandas.GeoDataFrame:
    with TemporaryDirectory() as directory:
        extract_zip(zip_path, Path(directory))
        shapefile = find_shapefile(Path(directory))
        check_shapefile_parts(shapefile)
        return read_layer(shapefile)
