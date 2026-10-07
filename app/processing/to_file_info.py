from app.schemas.file_info import FileInfo
from app.schemas.file_record import FileRecord


def to_file_info(record: FileRecord) -> FileInfo:
    return FileInfo(**record.model_dump(include=set(FileInfo.model_fields)))
