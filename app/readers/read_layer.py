from pathlib import Path

import geopandas
import pyogrio

from app.errors.unreadable_file_error import UnreadableFileError


def read_layer(path: Path, layer: str | None = None) -> geopandas.GeoDataFrame:
    try:
        return pyogrio.read_dataframe(path, layer=layer)
    except Exception as error:
        raise UnreadableFileError(f"The file could not be read: {error}") from error
