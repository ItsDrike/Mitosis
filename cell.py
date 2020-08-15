import typing as t
from random import randint, choice

from util import Colors, euclidean_distance


class Cell:
    DEACCELERATION_RATE = 0.1

    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        color: Colors.ColorType = Colors.BLUE,
        x_speed: float = 0,
        y_speed: float = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.x_positive = 1 if x_speed > 0 else -1
        self.y_positive = 1 if y_speed > 0 else -1

        self.x_speed = abs(x_speed)
        self.y_speed = abs(y_speed)

    def mitosis(
        self,
        new_color: t.Optional[Colors.ColorType] = None
    ) -> t.Tuple["Cell", "Cell"]:
        """Handle cell splitting in mitosis process"""
        new_radius = self.radius * 0.8
        new_color = new_color if new_color else self.color

        # Compute speeds so that when vectors are added, result will be 0
        x_speed = randint(0, round(self.radius))
        y_speed = self.radius - x_speed

        x_speed /= 8
        y_speed /= 8

        x_mult = choice([1, -1])
        y_mult = choice([1, -1])

        x_speed *= x_mult
        y_speed *= y_mult

        cell_1 = Cell(self.x, self.y, new_radius, new_color, x_speed, y_speed)
        cell_2 = Cell(self.x, self.y, new_radius, new_color, x_speed * -1, y_speed * -1)

        return (cell_1, cell_2)

    def move(self) -> None:
        """Movement of the cells"""
        if self.x_speed < 0:
            self.x_speed = 0
        if self.y_speed < 0:
            self.y_speed = 0

        if self.x_speed:
            self.x += self.x_speed * self.x_positive
            self.x_speed -= self.DEACCELERATION_RATE
        if self.y_speed:
            self.y += self.y_speed * self.y_positive
            self.y_speed -= self.DEACCELERATION_RATE

    @property
    def shape(self) -> t.Tuple[t.Tuple[int, int], int]:
        return ((round(self.x), round(self.y)), round(self.radius))

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
