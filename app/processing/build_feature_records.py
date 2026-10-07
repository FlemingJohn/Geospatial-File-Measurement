import geopandas

from app.processing.build_feature_record import build_feature_record
from app.processing.get_properties import get_properties
from app.schemas.feature_record import FeatureRecord


def build_feature_records(
    source: geopandas.GeoDataFrame, geographic: geopandas.GeoDataFrame, crs_label: str
) -> list[FeatureRecord]:
    properties = get_properties(source)
    return [
        build_feature_record(
            position + 1,
            properties[position],
            source.geometry.iloc[position],
            geographic.geometry.iloc[position],
            crs_label,
        )
        for position in range(len(source))
    ]
