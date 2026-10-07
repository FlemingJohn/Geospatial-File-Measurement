from pydantic import BaseModel

from app.schemas.feature_record import FeatureRecord
from app.schemas.measurement_totals import MeasurementTotals


class FileMeasurementsResponse(BaseModel):
    id: str
    filename: str
    crs: str
    measurement_method: str
    warnings: list[str]
    features: list[FeatureRecord]
    totals: MeasurementTotals
