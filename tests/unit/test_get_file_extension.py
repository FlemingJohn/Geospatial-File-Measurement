import pytest

from app.uploads.get_file_extension import get_file_extension


@pytest.mark.parametrize(
    "filename, expected",
    [("map.kml", ".kml"), ("MAP.KML", ".kml"), ("parcels.zip", ".zip"), ("notes", ""), (None, "")],
)
def test_extension_is_lower_case_or_empty(filename, expected):
    assert get_file_extension(filename) == expected
