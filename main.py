from contextlib import suppress

import pygame

from cell import Cell
from util import Colors

CELLS = 100
WIDTH, HEIGHT = 1200, 900
TICK_RATE = 100


class Game:
    def __init__(self, width: int, height: int, fps: int) -> None:
        self.size = self.width, self.height = width, height

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.fps_clock = pygame.time.Clock()
        self.tick_rate = fps

        self.running = True

    def handle_user_event(self) -> None:
        """Handle pygame events (f.e.: quit, click)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            # Start mitosis on mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                with suppress(IndexError):
                    clicked_cell = [
                        cell for cell in self.cells
                        if cell.rect.collidepoint(pos)
                    ]
                    self.mitosis(clicked_cell[0])
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    for cell in self.cells[:]:
                        self.mitosis(cell)

    def redraw_screen(self) -> None:
        """
        Redraw all cells on the screen.

        This does not update the screen, it only redraws it.
        """
        self.screen.fill(Colors.GREY)

        for cell in self.cells:
            cell.rect = pygame.draw.circle(self.screen, cell.color, *cell.shape)

    def update_screen(self, tick: bool = True) -> None:
        """
        Update the screen accordingly to `redraw_screen`
        also check for user event and tick (if not specified otherwise)
        """

        self.handle_user_event()

        if not self.running:
            return

        self.redraw_screen()
        pygame.display.update()
        if tick:
            self.fps_clock.tick(self.tick_rate)

    def mitosis(self, cell: Cell) -> None:
        self.cells.remove(cell)
        split_cells = cell.mitosis()

        for split_cell in split_cells:
            self.cells.append(split_cell)

    def main(self, cell_amt: int) -> None:
        # Make the cells
        self.cells = []
        for _ in range(cell_amt):
            cell = Cell.make_cell(self.width, self.height, self.cells)
            self.cells.append(cell)

        # Main game loop
        while self.running:
            for cell in self.cells[:]:
                cell.move()
                if any([
                    not (-cell.radius * 2 < cell.y < self.height + cell.radius * 2),
                    not (-cell.radius * 2 < cell.x < self.width + cell.radius * 2),
                ]):
                    self.cells.remove(cell)

            self.update_screen()


game = Game(WIDTH, HEIGHT, TICK_RATE)

with suppress(KeyboardInterrupt):
    game.main(CELLS)

print("\nStopped")
pygame.quit()
