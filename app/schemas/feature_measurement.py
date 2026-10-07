from pydantic import BaseModel


class FeatureMeasurement(BaseModel):
    area_square_meters: float | None
    area_hectares: float | None
    perimeter_meters: float | None
    length_meters: float | None
