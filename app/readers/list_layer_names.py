from pathlib import Path

import pyogrio

from app.errors.unreadable_file_error import UnreadableFileError


def list_layer_names(path: Path) -> list[str]:
    try:
        return [str(name) for name, _ in pyogrio.list_layers(path)]
    except Exception as error:
        raise UnreadableFileError(f"The KML file could not be read: {error}") from error
