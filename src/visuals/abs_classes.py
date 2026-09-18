import pygame as pg
from abc import ABC
from .game_layout import GameLayout


class Animation(ABC):
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, frames: int, sprites_n: int, looped: bool = True) -> None:
        if looped:
            self.current_frame = (self.current_frame + frames) % sprites_n
        else:
            self.current_frame = (self.current_frame + frames)

    def update_time(self, dt: float) -> None:
        self.animation_elapsed = self.animation_elapsed + dt * 1000
