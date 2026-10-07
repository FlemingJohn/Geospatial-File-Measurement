from pathlib import Path

from app.crs.get_crs_label import get_crs_label
from app.crs.get_crs_warnings import get_crs_warnings
from app.crs.to_geographic import to_geographic
from app.measurement.build_totals import build_totals
from app.measurement.measurement_method import MEASUREMENT_METHOD
from app.processing.build_feature_records import build_feature_records
from app.processing.prepare_features import prepare_features
from app.readers.read_file import read_file
from app.schemas.file_record import FileRecord


def process_saved_file(file_id: str, saved_path: Path, filename: str) -> FileRecord:
    source = prepare_features(read_file(saved_path))
    crs_label = get_crs_label(source)
    records = build_feature_records(source, to_geographic(source), crs_label)
    return FileRecord(
        id=file_id,
        filename=filename,
        feature_count=len(records),
        crs=crs_label,
        status="COMPLETED",
        warnings=get_crs_warnings(source),
        measurement_method=MEASUREMENT_METHOD,
        features=records,
        totals=build_totals(records),
    )
