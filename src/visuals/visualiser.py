import pygame as pg
from shared_types import Grid
from .game_layout import GameLayout
from .maze_view import MazeView
from .entity_view import EntityView
from .event_handler import EventHandler


class Visualiser():
    def __init__(self) -> None:
        self.grid: Grid

        self.width: int = 800
        self.height: int = 800
        self.screen = pg.display.set_mode((self.width, self.height))

        self.game_layout: GameLayout
        self.maze_view: MazeView
        self.entity_view: EntityView
        self.event_handler: EventHandler

    def main_loop(self) -> None:
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")

        while (True):
            self.event_handler.event_handling()
            self.screen.fill('black')
            self.maze_view.draw_maze()
            self.entity_view.draw_entities()

            pg.display.flip()

            clock.tick(60)

    def set_cur_grid(self, grid: Grid) -> None:
        self.grid = grid
        self.game_layout = GameLayout(self.grid,
                                      self.width, self.height)
        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)
        self.event_handler = EventHandler(self.screen)
