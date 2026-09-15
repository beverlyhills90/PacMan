import pygame as pg
import sys
from shared_types import Direction
from game import Game


class EventHandler():
    def __init__(self, screen: pg.Surface, game: Game) -> None:
        self.screen = screen
        self.game = game

    def event_handling(self, dt: float) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # if event.type == pg.KEYDOWN:
        keys = pg.key.get_pressed()
        intent = None
        if keys[pg.K_UP]:
            intent = "up"
        if keys[pg.K_DOWN]:
            intent = "down"
        if keys[pg.K_LEFT]:
            intent = "left"
        if keys[pg.K_RIGHT]:
            intent = "right"
        self.game.update(dt, intent)
