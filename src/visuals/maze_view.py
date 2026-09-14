from shared_types import Grid, Tile
from .game_layout import GameLayaout
import pygame as pg
from .errors import VisulisationError


class MazeView():
    def __init__(self, grid: Grid, game_layout: GameLayaout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayaout = game_layout
        self.screen: pg.Surface = screen

    def draw_maze(self) -> None:
        self.game_layout.get_tile_size()

        grid_h = self.game_layout.grid_h
        for i in range(grid_h):
            self.draw_row(i)

    def draw_row(self, row_num: int) -> None:
        row = self.grid[row_num]
        tile_size = self.game_layout.tile_size
        x = self.game_layout.get_offset_x()
        y = (self.game_layout.get_offset_y() + (tile_size * row_num))
        for i in range(len(row)):
            if row_num == 0:
                self.draw_upper_wall(x, y)
            if row_num == self.game_layout.grid_h - 1:
                self.draw_down_wall(x, y)
            if i == 0:
                self.draw_left_wall(x, y)
            if i == len(row) - 1:
                self.draw_right_wall(x, y)
            if row[i] == "floor":
                self.decide_wall(x, y, i, row_num)
            x += tile_size

    def decide_wall(self, x: int, y: int, tile_num: int, row_num: int) -> None:
        up_tile = self.grid[row_num - 1][tile_num]
        r_tile = self.grid[row_num][tile_num + 1]
        down_tile = self.grid[row_num+1][tile_num]
        l_tile = self.grid[row_num][tile_num - 1]
        if up_tile == "wall":
            self.draw_upper_wall(x, y)
        if r_tile == "wall":
            self.draw_right_wall(x, y)
        if down_tile == "wall":
            self.draw_down_wall(x, y)
        if l_tile == "wall":
            self.draw_left_wall(x, y)

    def draw_left_wall(self, x: int, y: int) -> None:
        tile_size = self.game_layout.tile_size
        pg.draw.line(self.screen, "white", (x, y), (x, y + tile_size))

    def draw_right_wall(self, x: int, y: int) -> None:
        tile_size = self.game_layout.tile_size
        pg.draw.line(self.screen, "white", (x + tile_size, y), (x + tile_size, y + tile_size))

    def draw_down_wall(self, x: int, y: int) -> None:
        tile_size = self.game_layout.tile_size
        pg.draw.line(self.screen, "white", (x, y + tile_size), (x + tile_size, y + tile_size))

    def draw_upper_wall(self, x: int, y: int) -> None:
        tile_size = self.game_layout.tile_size
        pg.draw.line(self.screen, "white", (x, y), (x + tile_size, y))

    """def draw_upper_wall(self, row: list[Tile]) -> None:
        x = self.game_layout.get_offset_x()
        y = self.game_layout.get_offset_y()
        tile_size = self.game_layout.tile_size
        for tile in row:
            if tile == "wall":
                pg.draw.line(self.screen, "white",
                             (x, y), (x + tile_size, y))
                x += tile_size
            else:
                raise VisulisationError("Missing border wall, something went "
                                        "wrong somewhere on genarating")"""
