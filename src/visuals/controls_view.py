import pygame as pg
from .buttons import MenuButton


class ControlsView():
    def __init__(self, screen: pg.Surface) -> None:
        self.screen: pg.Surface = screen
        self.controls_list: list[MenuButton]
