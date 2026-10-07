import shutil
from pathlib import Path

import geopandas


def build_shapefile_zip(features: geopandas.GeoDataFrame, directory: Path) -> Path:
    folder = directory / "parcels"
    folder.mkdir()
    features.to_file(folder / "parcels.shp")
    archive = shutil.make_archive(str(directory / "parcels"), "zip", folder)
    return Path(archive)
