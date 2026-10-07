from fastapi import APIRouter

from app.processing.to_file_info import to_file_info
from app.schemas.file_info import FileInfo
from app.storage.load_file_record import load_file_record

router = APIRouter(prefix="/api/files")


@router.get("/{file_id}/", response_model=FileInfo)
def get_file_info(file_id: str) -> FileInfo:
    return to_file_info(load_file_record(file_id))
