from .menu_view import MenuView
import pygame as pg
from shared_types import Grid, VisualState
from .game_layout import GameLayout
from .maze_view import MazeView
from .entity_view import EntityView
from .highscore_view import HighscoreView
from .victory_view import VictoryView
from .buttons import Fonts
from .event_handler import EventHandler
from core.player import Player
from game import Game
import sys


class Visualiser():
    def __init__(self, game: Game, player: Player) -> None:
        self.grid: Grid

        self.width: int = 800
        self.height: int = 800
        self.screen = pg.display.set_mode((self.width, self.height))

        self.game_layout: GameLayout
        self.maze_view: MazeView
        self.entity_view: EntityView
        self.event_handler: EventHandler

        self.fonts = Fonts()
        self.menu_view: MenuView = MenuView(self.screen, self.fonts)
        self.highscore_view: HighscoreView = HighscoreView(self.screen, self.fonts)
        self.victory_view = VictoryView(self.screen, self.fonts)
        self.game: Game = game
        self.player: Player = player

        self.state: VisualState = "victory_screen"

    def main_loop(self) -> None:
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")
        self.set_new_level()

        while (True):
            snapshot = self.game.snapshot()
            print(snapshot.status)
            if snapshot.status == "level_won":
                self.set_new_level()
            if snapshot.status == "victory":
                self.state = "victory_screen"
            dt: float = clock.tick(60) / 1000
            new_state = self.event_handler.event_handling(dt, self.state)
            if new_state is not None:
                self.state = new_state
            self.screen.fill('black')

            self.visual(dt)

            pg.display.flip()

    def visual(self, dt: float) -> None:
        if self.state == "menu":
            mouse_pos = pg.mouse.get_pos()
            self.menu_view.draw_menu(mouse_pos)

        elif self.state == "start":
            self.maze_view.draw_maze()
            self.entity_view.draw_entities(self.game, dt)

        elif self.state == "exit":
            pg.quit()
            sys.exit()

        elif self.state == "highscore":
            mouse_pos = pg.mouse.get_pos()
            self.highscore_view.draw_highscore(mouse_pos)

        elif self.state == "victory_screen":
            mouse_pos = pg.mouse.get_pos()
            self.maze_view.draw_maze()
            self.entity_view.draw_entities(self.game, dt)
            self.victory_view.draw_victory(mouse_pos)

    def set_new_level(self) -> None:
        snapshot = self.game.snapshot()
        self.grid = snapshot.grid

        self.game_layout = GameLayout(self.grid,
                                      self.width, self.height)
        self.game_layout.get_tile_size()

        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)

        self.event_handler = EventHandler(
            self.screen, self.game, self.menu_view, self.highscore_view)
