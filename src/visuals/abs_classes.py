import pygame as pg
from abc import ABC
from .game_layout import GameLayout


class Animation(ABC):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout,) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.game_layout: GameLayout = game_layout
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, frames: int, sprites_n: int) -> None:
        self.current_frame = (self.current_frame + frames) % sprites_n

    def update_time(self, dt: float) -> None:
        self.animation_elapsed = self.animation_elapsed + dt * 1000
