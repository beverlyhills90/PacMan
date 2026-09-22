import pygame as pg
import sys

from shared_types import Grid, VisualState
from game import Game
from core.player import Player
from parsing import Config

from .menu_view import MenuView
from .game_layout import GameLayout
from .maze_view import MazeView
from .entity_view import EntityView
from .highscore_view import HighscoreView
from .victory_view import VictoryView
from .hud_view import HudView
from .countdown_view import Countdown

from .buttons import Fonts

from .event_handler import EventHandler


class Visualiser():
    def __init__(self, player: Player, config: Config) -> None:
        self.grid: Grid
        self.config: Config = config

        self.width: int = 800
        self.height: int = 800
        self.screen = pg.display.set_mode((self.width, self.height))

        self.game_layout: GameLayout
        self.maze_view: MazeView
        self.entity_view: EntityView
        self.hud_view: HudView
        self.game: Game = Game(config, 3, 1)

        self.event_handler: EventHandler

        self.fonts = Fonts()
        self.menu_view: MenuView = MenuView(self.screen, self.fonts)
        self.highscore_view: HighscoreView = HighscoreView(self.screen, self.fonts)
        self.victory_view = VictoryView(self.screen, self.fonts)
        self.countdown_view = Countdown(self.screen, self.game)
        self.player: Player = player

        self.state: VisualState = "victory_screen"

    def main_loop(self) -> None:
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")
        self.set_new_level()

        while (True):
            print(self.game.status)
            dt: float = clock.tick(60) / 1000
            self.screen.fill('black')
            new_state = self.event_handler.event_handling(dt, self.state)

            if new_state is not None:
                if new_state == "menu":
                    self.refresh_game()
                    self.set_new_level()
                self.state = new_state

            if self.state == "start":
                self.state = "playing"

            if self.state == "playing":
                self.game_logic()

            self.visual(dt)

            pg.display.flip()

    def game_logic(self) -> None:
        snapshot = self.game.snapshot()

        if snapshot.status == "level_won":
            self.game.next_level()
            self.set_new_level()
            self.countdown_view.reset_animation()

        if snapshot.status == "game_over":
            self.state = "victory_screen"

        if snapshot.status == "dead":
            self.game.respawn()
            self.countdown_view.reset_animation()

    def visual(self, dt: float) -> None:
        mouse_pos = pg.mouse.get_pos()
        snapshot = self.game.snapshot()
        # print(self.game.status)

        if self.state == "menu":
            self.menu_view.draw_menu(mouse_pos)

        elif self.state == "playing":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)
            self.countdown_view.draw_countdown(dt)

        elif self.state == "exit":
            pg.quit()
            sys.exit()

        elif self.state == "highscore":
            self.highscore_view.draw_highscore_menu(mouse_pos, dt)

        elif self.state == "victory_screen":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)

            self.victory_view.draw_victory(mouse_pos, dt)

    def set_new_level(self) -> None:
        snapshot = self.game.snapshot()
        self.grid = snapshot.grid

        self.game_layout = GameLayout(self.grid,
                                      self.width, self.height)
        self.game_layout.get_tile_size()

        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)
        self.hud_view = HudView(self.screen, self.fonts, self.game_layout)

        self.event_handler = EventHandler(
            self.screen, self.game, self.menu_view, self.highscore_view)

    def refresh_game(self) -> None:
        self.game = Game(self.config)
        self.countdown_view = Countdown(self.screen, self.game)
