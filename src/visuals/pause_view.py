import pygame as pg
from .buttons import Fonts, MenuButton


class PauseView():
    def __init__(self, screen: pg.Surface,) -> None:
        self.screen: pg.Surface = screen
