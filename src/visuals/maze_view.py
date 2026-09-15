from shared_types import Grid
from .game_layout import GameLayout
import pygame as pg
from enum import IntFlag


class WallConnection(IntFlag):
    EMPTY = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class MazeView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen
        self.wall_sprites: list[pg.Surface] = [pg.transform.scale(pg.image.load(
            f"visuals/sprites/tiles/wall_{i:02d}.png").convert_alpha(),
            (35, 35)) for i in range(16)]

        self.wall_color = "white"

    def draw_maze(self) -> None:
        self.game_layout.get_tile_size()
        grid_h = self.game_layout.grid_h
        grid_w = self.game_layout.grid_w
        x = self.game_layout.get_offset_x()
        y = self.game_layout.get_offset_y()
        tile_size = self.game_layout.tile_size
        for row_n in range(grid_h):
            row = self.grid[row_n]
            for col_n in range(grid_w):
                if row[col_n] == "wall":
                    mask: WallConnection = WallConnection.EMPTY
                    if col_n - 1 > -1 and row[col_n-1] == "wall":
                        mask |= WallConnection.LEFT
                    if col_n + 1 < grid_w and row[col_n+1] == "wall":
                        mask |= WallConnection.RIGHT
                    if row_n - 1 > -1 and self.grid[row_n-1][col_n] == "wall":
                        mask |= WallConnection.UP
                    if row_n + 1 < grid_h and self.grid[row_n+1][col_n] == "wall":
                        mask |= WallConnection.DOWN
                    self.screen.blit(self.wall_sprites[mask], (x, y))
                    wall_hitbox = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
                    wall_hitbox.fill((0, 50, 0, 128))
                    self.screen.blit(wall_hitbox, (x, y))
                x += tile_size
            x = self.game_layout.get_offset_x()
            y += tile_size
