from pathlib import Path

from app.errors.invalid_zip_error import InvalidZipError
from app.errors.missing_shapefile_parts_error import MissingShapefilePartsError


def find_shapefile(directory: Path) -> Path:
    shapefiles = sorted(
        path for path in directory.rglob("*") if is_shapefile(path)
    )
    if not shapefiles:
        raise MissingShapefilePartsError("The zip archive does not contain a .shp file")
    if len(shapefiles) > 1:
        raise InvalidZipError("The zip archive must contain exactly one shapefile")
    return shapefiles[0]


def is_shapefile(path: Path) -> bool:
    return path.suffix.lower() == ".shp" and "__MACOSX" not in path.parts
