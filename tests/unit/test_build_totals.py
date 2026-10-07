from app.measurement.build_totals import build_totals
from app.schemas.feature_measurement import FeatureMeasurement
from app.schemas.feature_record import FeatureRecord


def make_record(status, **measurement_values) -> FeatureRecord:
    measurement = None
    if status == "MEASURED":
        defaults = dict(area_square_meters=None, area_hectares=None, perimeter_meters=None, length_meters=None)
        measurement = FeatureMeasurement(**{**defaults, **measurement_values})
    return FeatureRecord(
        id=1, geometry_type=None, geometry=None, crs="EPSG:4326", properties={},
        measurement_status=status, projected_crs=None, measurement=measurement,
    )


def test_totals_add_up_each_kind_of_measurement():
    records = [
        make_record("MEASURED", area_square_meters=20_000, perimeter_meters=600),
        make_record("MEASURED", length_meters=150.5),
        make_record("NOT_REQUIRED"),
        make_record("UNSUPPORTED"),
    ]
    totals = build_totals(records)
    assert totals.feature_count == 4
    assert totals.measured_feature_count == 2
    assert totals.unsupported_feature_count == 1
    assert totals.total_area_square_meters == 20_000
    assert totals.total_area_hectares == 2
    assert totals.total_perimeter_meters == 600
    assert totals.total_length_meters == 150.5
