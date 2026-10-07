from app.schemas.feature_record import FeatureRecord
from app.schemas.measurement_totals import MeasurementTotals

SQUARE_METERS_PER_HECTARE = 10_000


def build_totals(features: list[FeatureRecord]) -> MeasurementTotals:
    measurements = [feature.measurement for feature in features if feature.measurement]
    area = sum(measurement.area_square_meters or 0 for measurement in measurements)
    return MeasurementTotals(
        feature_count=len(features),
        measured_feature_count=len(measurements),
        unsupported_feature_count=count_unsupported(features),
        total_area_square_meters=round(area, 3),
        total_area_hectares=round(area / SQUARE_METERS_PER_HECTARE, 6),
        total_perimeter_meters=round(sum(item.perimeter_meters or 0 for item in measurements), 3),
        total_length_meters=round(sum(item.length_meters or 0 for item in measurements), 3),
    )


def count_unsupported(features: list[FeatureRecord]) -> int:
    return sum(feature.measurement_status == "UNSUPPORTED" for feature in features)
