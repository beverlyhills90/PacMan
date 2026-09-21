from shared_types import Grid, GameState, Pos
from .game_layout import GameLayout
import pygame as pg
from enum import IntFlag
from pathlib import Path
from .abs_classes import Animation

SUPER_GUM_N = 2
SUPER_GUM_SEQUENCY = (0, 1, 0)
SUPER_GUM_FRAME_DUR = 180


class WallConnection(IntFlag):
    EMPTY = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Gum():
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen

        self.path_sprite: Path = Path(__file__).resolve().parent / "sprites" / "pacgums"
        self.gum_sprite: pg.Surface = pg.transform.scale(pg.image.load(
            f"{self.path_sprite}/pacgum.png").convert_alpha(),
            (game_layout.tile_size, game_layout.tile_size))

    def draw_pacgum(self, pos: Pos) -> None:
        x, y = self.game_layout.tiles_to_coordinates(pos)
        self.screen.blit(self.gum_sprite, (x, y))


class SuperGum(Animation):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        super().__init__(screen)
        self.game_layout: GameLayout = game_layout

        self.path_sprite: Path = Path(__file__).resolve().parent / "sprites" / "pacgums"
        self.super_gum_sprites: list[pg.Surface] = [pg.transform.scale(pg.image.load(
            f"{self.path_sprite}/super_pacgum_{i}.png").convert_alpha(),
            (game_layout.tile_size, game_layout.tile_size)) for i in range(SUPER_GUM_N)]

    def draw_super_pacgum(self, pos: Pos, dt: float) -> None:
        x, y = self.game_layout.tiles_to_coordinates(pos)
        self.update_time(dt)
        frames = 0
        while self.animation_elapsed >= SUPER_GUM_FRAME_DUR:
            frames += 1
            self.animation_elapsed -= SUPER_GUM_FRAME_DUR
        self.update_frame(frames, SUPER_GUM_SEQUENCY)
        self.screen.blit(self.super_gum_sprites[self.current_frame], (x, y))


class MazeView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen
        self.size = game_layout.tile_size
        self.wall_sprites: list[pg.Surface] = [pg.transform.scale(pg.image.load(
            f"visuals/sprites/tiles/wall_{i:02d}.png").convert_alpha(),
            (self.size, self.size)) for i in range(16)]
        self.gum: Gum = Gum(screen, game_layout)
        self.super_gum: SuperGum = SuperGum(screen, game_layout)

    def draw_maze(self, snapshot: GameState, dt: float) -> None:
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

                x += tile_size

            x = self.game_layout.get_offset_x()
            y += tile_size

        self._draw_gums(snapshot, dt)

    def _draw_gums(self, snapshot: GameState, dt: float) -> None:
        for pos in snapshot.pacgums:
            self.gum.draw_pacgum(pos)

        for pos in snapshot.super_pacgums:
            self.super_gum.draw_super_pacgum(pos, dt)
