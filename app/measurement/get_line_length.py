from shapely.geometry import LineString


def get_line_length(line: LineString) -> float:
    return line.length
