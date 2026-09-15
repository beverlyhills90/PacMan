import pygame as pg
import sys
from shared_types import Direction


class EventHandler():
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen

    def event_handling(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.K_UP:
                pass
