from app.schemas.file_measurements_response import FileMeasurementsResponse
from app.schemas.file_record import FileRecord


def to_file_measurements(record: FileRecord) -> FileMeasurementsResponse:
    fields = set(FileMeasurementsResponse.model_fields)
    return FileMeasurementsResponse.model_validate(record.model_dump(include=fields))
