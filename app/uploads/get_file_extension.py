from pathlib import Path


def get_file_extension(filename: str | None) -> str:
    return Path(filename or "").suffix.lower()
