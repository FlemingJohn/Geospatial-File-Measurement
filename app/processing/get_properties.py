import json

import geopandas


def get_properties(features: geopandas.GeoDataFrame) -> list[dict]:
    attributes = features.drop(columns=features.geometry.name)
    return json.loads(attributes.to_json(orient="records"))
