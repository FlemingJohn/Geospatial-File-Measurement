from tests.builders.build_kml_text import build_kml_text
from tests.builders.build_square_kml import SQUARE_PLACEMARK

LINE_PLACEMARK = (
    "<Placemark><name>Road</name><LineString><coordinates>"
    "0,0,0 0.01,0,0"
    "</coordinates></LineString></Placemark>"
)
POINT_PLACEMARK = "<Placemark><name>Well</name><Point><coordinates>77.59,12.97,0</coordinates></Point></Placemark>"
COLLECTION_PLACEMARK = (
    "<Placemark><name>Mixed</name><MultiGeometry>"
    "<Point><coordinates>1,1,0</coordinates></Point>"
    "<LineString><coordinates>1,1,0 1.01,1,0</coordinates></LineString>"
    "</MultiGeometry></Placemark>"
)
NO_GEOMETRY_PLACEMARK = "<Placemark><name>Nothing</name></Placemark>"


def build_mixed_kml() -> str:
    placemarks = (
        SQUARE_PLACEMARK + LINE_PLACEMARK + POINT_PLACEMARK + COLLECTION_PLACEMARK + NO_GEOMETRY_PLACEMARK
    )
    return build_kml_text(placemarks)
