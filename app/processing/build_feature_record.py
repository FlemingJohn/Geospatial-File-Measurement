from shapely.geometry.base import BaseGeometry

from app.crs.get_projected_epsg import get_projected_epsg
from app.crs.project_geometry import project_geometry
from app.measurement.get_measurement_status import get_measurement_status
from app.measurement.measure_geometry import measure_geometry
from app.processing.get_geometry_json import get_geometry_json
from app.schemas.feature_record import FeatureRecord


def build_feature_record(
    feature_id: int,
    properties: dict,
    source_geometry: BaseGeometry | None,
    geographic_geometry: BaseGeometry | None,
    crs_label: str,
) -> FeatureRecord:
    status = get_measurement_status(geographic_geometry)
    epsg = get_projected_epsg(geographic_geometry) if status == "MEASURED" else None
    return FeatureRecord(
        id=feature_id,
        geometry_type=None if source_geometry is None else source_geometry.geom_type,
        geometry=get_geometry_json(source_geometry),
        crs=crs_label,
        properties=properties,
        measurement_status=status,
        projected_crs=None if epsg is None else f"EPSG:{epsg}",
        measurement=None if epsg is None else measure_geometry(project_geometry(geographic_geometry, epsg)),
    )
