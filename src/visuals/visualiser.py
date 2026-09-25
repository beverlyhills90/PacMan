import sys

import pygame as pg

from src.core.player import Player
from src.core.sound import Sounds
from src.game import Game
from src.parsing import Config
from src.shared_types import Grid, VisualState

from .buttons import Fonts
from .controls_view import ControlsView
from .countdown_view import Countdown
from .entity_view import EntityView
from .event_handler import EventHandler
from .game_layout import GameLayout
from .highscore_view import HighscoreView
from .hud_view import HudView
from .maze_view import MazeView
from .menu_view import MenuView
from .name_input import InputName
from .victory_view import VictoryView
from .pause_view import PauseView


class Visualiser:
    """Owns the window, the game and every screen, and runs the main loop."""

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
        self.game: Game = Game(config)
        self.sounds: Sounds = Sounds()

        self.event_handler: EventHandler

        self.fonts = Fonts()
        self.menu_view: MenuView = MenuView(
            self.screen, self.fonts, self.sounds
        )
        self.highscore_view: HighscoreView = HighscoreView(
            self.screen, self.fonts, config.highscore_filename
        )
        self.name_input: InputName = InputName(self.screen, self.fonts)
        self.victory_view = VictoryView(self.screen, self.fonts)
        self.countdown_view = Countdown(self.screen, self.game)
        self.controls_view = ControlsView(self.screen, self.fonts)
        self.pause_view = PauseView(self.screen, self.fonts)

        self.player: Player = player
        self.name: list[str] = []

        self.state: VisualState = "menu"

    def main_loop(self) -> None:
        """Run the game at 60 FPS until the window is closed."""
        clock = pg.time.Clock()
        pg.display.set_caption("Pacman")
        self.set_new_level()

        while True:
            dt: float = clock.tick(60) / 1000
            self.screen.fill("black")
            new_state = self.event_handler.event_handling(dt, self.state)
            print(self.game.score)
            if new_state is not None:
                if new_state == "menu" and self.state == "name_input":
                    self.name = self.name_input.name
                    self.game.save_score("".join(self.name))
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
        """React to the game status: next level, respawn, win or loss."""
        snapshot = self.game.snapshot()

        if snapshot.status == "level_won":
            self.game.next_level()
            self.set_new_level()
            self.countdown_view.reset_animation()

        if snapshot.status == "game_over":
            self.state = "lost_screen"

        if snapshot.status == "victory":
            self.state = "victory_screen"

        if snapshot.status == "dead":
            self.game.respawn()
            self.countdown_view.reset_animation()

        if snapshot.status == "pause":
            self.state = "pause"

    def visual(self, dt: float) -> None:
        """Draw the current screen.

        Args:
            dt: Seconds elapsed since the previous frame.
        """
        mouse_pos = pg.mouse.get_pos()
        snapshot = self.game.snapshot()

        if self.state == "name_input":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)
            self.name_input.draw_imput_screen(mouse_pos)

        if self.state == "menu":
            self.menu_view.draw_menu(mouse_pos)

        if self.state == "playing":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)
            self.countdown_view.draw_countdown(dt)

        if self.state == "pause":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)
            self.pause_view.draw_pause(mouse_pos)

        if self.state == "exit":
            pg.quit()
            sys.exit()

        if self.state == "highscore":
            self.highscore_view.draw_highscore_menu(mouse_pos, dt)

        if self.state == "victory_screen":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)

            self.victory_view.draw_victory(mouse_pos, dt, snapshot)
        if self.state == "lost_screen":
            self.maze_view.draw_maze(snapshot, dt)
            self.entity_view.draw_entities(snapshot, dt)
            self.hud_view.draw_hud(snapshot, mouse_pos)

            self.victory_view.draw_victory(mouse_pos, dt, snapshot, True)

        if self.state == "controls":
            self.controls_view.draw_control_menu(mouse_pos)

    def set_new_level(self) -> None:
        """Rebuild the views that depend on the current maze."""
        snapshot = self.game.snapshot()
        self.grid = snapshot.grid

        self.game_layout = GameLayout(self.grid, self.width, self.height)
        self.game_layout.get_tile_size()

        self.maze_view = MazeView(self.grid, self.game_layout, self.screen)
        self.entity_view = EntityView(self.grid, self.game_layout, self.screen)
        self.hud_view = HudView(self.screen, self.fonts, self.game_layout)
        self.highscore_view = HighscoreView(
            self.screen, self.fonts, self.config.highscore_filename
        )
        self.event_handler = EventHandler(
            self.screen,
            self.game,
            self.menu_view,
            self.highscore_view,
            self.controls_view,
            self.name_input,
            self.pause_view
        )

    def refresh_game(self) -> None:
        """Start a new game from level 1."""
        self.game = Game(self.config)
        self.countdown_view = Countdown(self.screen, self.game)
