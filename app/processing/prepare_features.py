import geopandas
import shapely

from app.errors.empty_file_error import EmptyFileError


def prepare_features(features: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
    if features.empty:
        raise EmptyFileError("The file does not contain any features")
    prepared = features.reset_index(drop=True)
    prepared.geometry = shapely.force_2d(prepared.geometry.values)
    return prepared
