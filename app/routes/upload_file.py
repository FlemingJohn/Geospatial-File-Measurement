from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, File, UploadFile

from app.processing.process_saved_file import process_saved_file
from app.processing.to_file_info import to_file_info
from app.schemas.file_info import FileInfo
from app.storage.make_file_id import make_file_id
from app.storage.save_file_record import save_file_record
from app.uploads.get_file_extension import get_file_extension
from app.uploads.save_upload import save_upload
from app.uploads.validate_extension import validate_extension

router = APIRouter(prefix="/api/files")


@router.post("/", response_model=FileInfo, status_code=201)
def upload_file(file: UploadFile = File(...)) -> FileInfo:
    extension = get_file_extension(file.filename)
    validate_extension(extension)
    with TemporaryDirectory() as directory:
        saved_path = save_upload(file.file, Path(directory) / f"upload{extension}")
        record = process_saved_file(make_file_id(), saved_path, file.filename)
    save_file_record(record)
    return to_file_info(record)
