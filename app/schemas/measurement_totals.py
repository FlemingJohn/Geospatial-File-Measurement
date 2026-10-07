from pydantic import BaseModel


class MeasurementTotals(BaseModel):
    feature_count: int
    measured_feature_count: int
    unsupported_feature_count: int
    total_area_square_meters: float
    total_area_hectares: float
    total_perimeter_meters: float
    total_length_meters: float
