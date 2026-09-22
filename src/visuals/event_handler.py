import sys

import pygame as pg

from game import Game
from shared_types import Direction, VisualState

from .highscore_view import HighscoreView
from .menu_view import MenuView


class EventHandler:
    def __init__(
        self,
        screen: pg.Surface,
        game: Game,
        menu_view: MenuView,
        highscore_view: HighscoreView,
    ) -> None:
        self.screen: pg.Surface = screen
        self.game: Game = game
        self.menu_view: MenuView = menu_view
        self.highscore_view: HighscoreView = highscore_view

    def event_handling(
        self, dt: float, state: VisualState
    ) -> VisualState | None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if state == "menu" and event.type == pg.MOUSEBUTTONUP:
                return self.menu_events(event)
            if state == "highscore" and event.type == pg.MOUSEBUTTONUP:
                return self.highscore_events(event)
            if state == "victory_screen" and event.type == pg.KEYDOWN:
                return self.victory_events()

        if state == "playing":
            return self.game_events(dt)
        return None

    def game_events(self, dt: float) -> VisualState | None:
        keys = pg.key.get_pressed()
        cheats = pg.key.get_just_released()
        intent: Direction | None = None
        if keys[pg.K_UP]:
            intent = "up"
        if keys[pg.K_DOWN]:
            intent = "down"
        if keys[pg.K_LEFT]:
            intent = "left"
        if keys[pg.K_RIGHT]:
            intent = "right"
        if keys[pg.K_ESCAPE]:
            self.game.pause()
        if cheats[pg.K_l]:
            self.game.cheat("level_skip")
        if cheats[pg.K_i]:
            self.game.cheat("inflives")
        if cheats[pg.K_1]:
            self.game.cheat("pluslive")
        if cheats[pg.K_0]:
            self.game.cheat("slow_ghosts")
        if cheats[pg.K_t]:
            self.game.cheat("inftime")
        self.game.update(dt, intent)
        return None

    def menu_events(self, event: pg.Event) -> VisualState | None:
        mouse_pos = event.pos
        if event.button == 1:
            return self.menu_view.handle_input(mouse_pos)
        return None

    def highscore_events(self, event: pg.Event) -> VisualState | None:
        mouse_pos = event.pos
        if event.button == 1:
            return self.highscore_view.handle_input(mouse_pos)
        return None

    def victory_events(self) -> VisualState | None:
        return "menu"
