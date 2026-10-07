from tests.builders.build_kml_text import build_kml_text

SQUARE_PLACEMARK = (
    "<Placemark><name>Square</name><Polygon><outerBoundaryIs><LinearRing><coordinates>"
    "0,0,0 0.001,0,0 0.001,0.001,0 0,0.001,0 0,0,0"
    "</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>"
)


def build_square_kml() -> str:
    return build_kml_text(SQUARE_PLACEMARK)
