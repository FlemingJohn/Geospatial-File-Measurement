import pytest

from app.errors.invalid_zip_error import InvalidZipError
from app.errors.missing_shapefile_parts_error import MissingShapefilePartsError
from app.readers.check_shapefile_parts import check_shapefile_parts
from app.readers.find_shapefile import find_shapefile


def test_shapefile_is_found_in_a_nested_folder(tmp_path):
    nested = tmp_path / "inner"
    nested.mkdir()
    (nested / "parcels.shp").write_bytes(b"")
    assert find_shapefile(tmp_path) == nested / "parcels.shp"


def test_missing_shapefile_is_reported(tmp_path):
    with pytest.raises(MissingShapefilePartsError):
        find_shapefile(tmp_path)


def test_two_shapefiles_are_rejected(tmp_path):
    (tmp_path / "a.shp").write_bytes(b"")
    (tmp_path / "b.shp").write_bytes(b"")
    with pytest.raises(InvalidZipError):
        find_shapefile(tmp_path)


def test_missing_companion_files_are_reported(tmp_path):
    shapefile = tmp_path / "parcels.shp"
    shapefile.write_bytes(b"")
    (tmp_path / "parcels.dbf").write_bytes(b"")
    with pytest.raises(MissingShapefilePartsError, match=".shx"):
        check_shapefile_parts(shapefile)
