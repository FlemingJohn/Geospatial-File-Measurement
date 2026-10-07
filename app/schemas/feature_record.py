from typing import Any

from pydantic import BaseModel

from app.schemas.feature_measurement import FeatureMeasurement
from app.schemas.measurement_status import MeasurementStatus


class FeatureRecord(BaseModel):
    id: int
    geometry_type: str | None
    geometry: dict[str, Any] | None
    crs: str
    properties: dict[str, Any]
    measurement_status: MeasurementStatus
    projected_crs: str | None
    measurement: FeatureMeasurement | None
