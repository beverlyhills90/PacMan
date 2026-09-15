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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.game.update(dt, "up")
                elif event.key == pg.K_DOWN:
                    self.game.update(dt, "down")
                elif event.key == pg.K_LEFT:
                    self.game.update(dt, "left")
                elif event.key == pg.K_RIGHT:
                    self.game.update(dt, "right")
            else:
                self.game.update(dt, None)
