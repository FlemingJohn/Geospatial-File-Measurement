from pydantic import BaseModel

from app.schemas.feature_record import FeatureRecord
from app.schemas.file_status import FileStatus
from app.schemas.measurement_totals import MeasurementTotals


class FileRecord(BaseModel):
    id: str
    filename: str
    feature_count: int
    crs: str
    status: FileStatus
    warnings: list[str]
    measurement_method: str
    features: list[FeatureRecord]
    totals: MeasurementTotals
