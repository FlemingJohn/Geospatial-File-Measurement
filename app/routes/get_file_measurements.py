from fastapi import APIRouter

from app.processing.to_file_measurements import to_file_measurements
from app.schemas.file_measurements_response import FileMeasurementsResponse
from app.storage.load_file_record import load_file_record

router = APIRouter(prefix="/api/files")


@router.get("/{file_id}/measurements/", response_model=FileMeasurementsResponse)
def get_file_measurements(file_id: str) -> FileMeasurementsResponse:
    return to_file_measurements(load_file_record(file_id))
