import pygame as pg
from shared_types import Grid
from .game_layout import GameLayout


class EntityView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen

        self.pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [pg.transform.scale(pg.image.load(
                f"visuals/sprites/pacman/pacman_{direction}_{frame}.png").convert_alpha(),
                (35, 35))
                for frame in range(4)]
            for direction in ("right", "down", "left", "up")
        }

    def draw_entities(self) -> None:
        self.draw_pacman()

    def draw_pacman(self) -> None:
        x, y = self.game_layout.get_grid_center()
        self.screen.blit(self.pacman_sprites["right"][0], (x, y))
