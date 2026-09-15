import pygame as pg
from shared_types import Grid, GameState, PacmanView
from .game_layout import GameLayout
from .maze_view import MazeView
from .entity_view import EntityView
from .event_handler import EventHandler
from core.player import Player
from game import Game
from parsing import Config
from core.world import find_start


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
        self.game: Game
        self.player: Player

    def main_loop(self) -> None:
        pg.init()
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")
        self.game_layout.get_tile_size()

        while (True):
            dt: float = clock.tick(60) / 1000
            self.event_handler.event_handling(dt)
            self.screen.fill('black')
            self.maze_view.draw_maze()
            self.entity_view.draw_entities(self.game)

            pg.display.flip()

    def set_cur_grid(self, grid: Grid, game: Game, player: Player) -> None:
        self.grid = grid
        self.game_layout = GameLayout(self.grid,
                                      self.width, self.height)
        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)
        self.player = player
        self.game = game
        self.event_handler = EventHandler(self.screen, self.game)
