from pydantic import BaseModel

from app.schemas.file_status import FileStatus


class FileInfo(BaseModel):
    id: str
    filename: str
    feature_count: int
    crs: str
    status: FileStatus
    warnings: list[str]
