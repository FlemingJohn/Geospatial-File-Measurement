import os
from pathlib import Path


def get_storage_directory() -> Path:
    return Path(os.environ.get("GEOSPATIAL_STORAGE_DIRECTORY", "storage"))
