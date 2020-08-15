import typing as t
from math import sqrt


def number_remap(
    value: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float
) -> float:
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


def euclidean_distance(
    point1_x: float,
    point1_y: float,
    point2_x: float,
    point2_y: float
) -> float:
    x_dist = abs(point1_x - point2_x)
    y_dist = abs(point1_y - point2_y)
    return sqrt(x_dist ** 2 + y_dist ** 2)


class Colors:
    GREY = 125, 125, 125
    BLUE = 100, 0, 255
    RED = 240, 20, 30
    BLACK = 0, 0, 0

    ColorType = t.Tuple[int, int, int]
