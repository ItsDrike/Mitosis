import typing as t
from util import Colors, euclidean_distance
from random import randint


class Cell:
    def __init__(self, x: int, y: int, radius: int, color: Colors.ColorType) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    @property
    def shape(self) -> t.Tuple[t.Tuple[int, int], int]:
        return ((self.x, self.y), self.radius)

    def _overlaps(self, other: "Cell") -> bool:
        """Check if 2 cells overlaps each other"""
        distance = euclidean_distance(self.x, self.y, other.x, other.y)
        radius_sum = self.radius + other.radius
        return distance <= radius_sum

    @classmethod
    def make_cell(cls, width: int, height: int, cells: t.List["Cell"]) -> "Cell":
        """
        This function creates a cell which
        doesn't overlap with other cells defined in `cells`.
        """
        r = randint(18, 38)
        x = randint(r, width - r)
        y = randint(r, height - r)
        cell = cls(x, y, r, Colors.BLUE)

        # Check for overlap
        for existing_cell in cells:
            if existing_cell._overlaps(cell):
                break
        else:
            return cell

        return cls.make_cell(width, height, cells)
