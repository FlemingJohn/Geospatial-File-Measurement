from pathlib import Path

import geopandas
import pandas

from app.readers.list_layer_names import list_layer_names
from app.readers.read_layer import read_layer


def read_kml(path: Path) -> geopandas.GeoDataFrame:
    layers = [read_layer(path, name) for name in list_layer_names(path)]
    filled_layers = [layer for layer in layers if not layer.empty]
    if not filled_layers:
        return geopandas.GeoDataFrame(geometry=[], crs="EPSG:4326")
    combined = pandas.concat(filled_layers, ignore_index=True)
    return geopandas.GeoDataFrame(combined, crs=filled_layers[0].crs)
