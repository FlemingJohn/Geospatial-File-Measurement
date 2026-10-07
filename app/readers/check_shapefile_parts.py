from pathlib import Path

from app.errors.missing_shapefile_parts_error import MissingShapefilePartsError

REQUIRED_SUFFIXES = (".shx", ".dbf")


def check_shapefile_parts(shapefile: Path) -> None:
    present = {path.suffix.lower() for path in shapefile.parent.iterdir() if path.stem == shapefile.stem}
    missing = [suffix for suffix in REQUIRED_SUFFIXES if suffix not in present]
    if missing:
        raise MissingShapefilePartsError(f"The shapefile is missing: {', '.join(missing)}")
