from shared_types import Grid
from .errors import VisulisationError


class GameLayout():
    def __init__(self, grid: Grid,
                 screen_w: int, screen_h: int) -> None:
        self.grid = grid
        self.grid_w = len(grid[0])
        self.grid_h = len(grid)
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.side_margin = 10
        self.bottom_margin = 50
        self.top_margin = 10

        self.tile_size: int
        self.wall_width: int

    def get_tile_size(self) -> None:
        tile_by_width = ((self.screen_w - self.side_margin * 2) // self.grid_w)
        tile_by_height = ((self.screen_h - self.top_margin - self.bottom_margin)
                          // self.grid_h)
        self.tile_size = min(tile_by_height, tile_by_width)
        self.wall_width = int(self.tile_size // 5)

    def get_offset_x(self) -> int:
        maze_width = self.tile_size * self.grid_w
        unused_width = self.screen_w - maze_width
        offset_x = unused_width // 2
        return offset_x

    def get_offset_y(self) -> int:
        return self.top_margin

    def get_grid_center(self) -> tuple[int, int]:
        x_tile = self.grid_w // 2
        y_tile = self.grid_h // 2
        if self.grid[y_tile][x_tile] == 'floor':
            return (self.get_offset_x() * x_tile, self.get_offset_y() * y_tile)
        radius = 1
        limiter = max(self.grid_h, self.grid_w)
        for radius in range(limiter + 1):
            for dx in range(-radius, radius + 1):
                vertical = radius - abs(dx)
                for dy in {vertical, -vertical}:
                    if (0 <= x_tile + dx < self.grid_w and 0 <= y_tile+dy < self.grid_h):
                        if self.grid[y_tile + dy][x_tile + dx] == 'floor':
                            return (self.get_offset_x() + (self.tile_size*(x_tile + dx)),
                                    self.get_offset_y() + (self.tile_size*(y_tile + dy)))

        raise VisulisationError("Couldnt find a place for pacman. Shouldnt happen...")
