from typing import Callable

from shapely.geometry.base import BaseGeometry

DECIMAL_PLACES = 3


def sum_measurements(parts: list[BaseGeometry], measure: Callable[[BaseGeometry], float]) -> float | None:
    if not parts:
        return None
    return round(sum(measure(part) for part in parts), DECIMAL_PLACES)
