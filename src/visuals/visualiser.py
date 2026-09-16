from .menu_view import MenuView
import pygame as pg
from shared_types import Grid, VisualState
from .game_layout import GameLayout
from .maze_view import MazeView
from .entity_view import EntityView
from .highscore_view import HighscoreView
from .event_handler import EventHandler
from core.player import Player
from game import Game
import sys


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
        self.menu_view: MenuView
        self.highscore_view: HighscoreView
        self.game: Game
        self.player: Player

        self.state: VisualState = "menu"

    def main_loop(self) -> None:
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")
        self.game_layout.get_tile_size()

        while (True):
            dt: float = clock.tick(60) / 1000
            new_state = self.event_handler.event_handling(dt, self.state)
            if new_state is not None:
                print(new_state)
                self.state = new_state
            self.screen.fill('black')

            self.visual()

            pg.display.flip()

    def visual(self) -> None:
        if self.state == "menu":
            mouse_pos = pg.mouse.get_pos()
            self.menu_view.draw_menu(mouse_pos)

        elif self.state == "start":
            self.maze_view.draw_maze()
            self.entity_view.draw_entities(self.game)

        elif self.state == "exit":
            pg.quit()
            sys.exit()

        elif self.state == "highscore":
            mouse_pos = pg.mouse.get_pos()
            self.highscore_view.draw_highscore(mouse_pos)

    def set_cur_grid(self, grid: Grid, game: Game, player: Player) -> None:
        self.grid = grid
        self.game_layout = GameLayout(self.grid,
                                      self.width, self.height)
        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)
        self.player = player
        self.game = game
        self.menu_view = MenuView(self.screen)
        self.highscore_view = HighscoreView(self.screen)
        self.event_handler = EventHandler(
            self.screen, self.game, self.menu_view, self.highscore_view)
