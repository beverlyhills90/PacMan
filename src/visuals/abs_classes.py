import pygame as pg
from abc import ABC
from .errors import VisulisationError


class Animation(ABC):
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, step: int, sequence: tuple[int, ...] | None) -> None:
        if sequence:
            self.current_frame = sequence[(self.current_frame + step) % len(sequence)]
        else:
            self.current_frame = (self.current_frame + step)

    def update_time(self, dt: float) -> None:
        self.animation_elapsed = self.animation_elapsed + dt * 1000
