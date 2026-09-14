import pygame as pg
from shared_types import Grid
from .game_layout import GameLayaout
from .maze_view import MazeView
import sys


class Visualiser():
    def __init__(self) -> None:
        self.grid: Grid

        self.width: int = 800
        self.height: int = 800
        self.screen = pg.display.set_mode((self.width, self.height))

        self.game_layout: GameLayaout
        self.maze_view: MazeView

    def main_loop(self) -> None:
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")

        while (True):
            self.event_handling()
            self.screen.fill('black')
            self.maze_view.draw_maze()

            pg.display.flip()

            clock.tick(60)

    def event_handling(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def set_cur_grid(self, grid: Grid) -> None:
        self.grid = grid
        self.game_layout = GameLayaout(self.grid,
                                       self.width, self.height)
        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
