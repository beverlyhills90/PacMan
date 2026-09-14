from shared_types import Grid


class GameLayaout():
    def __init__(self, grid: Grid,
                 screen_w: int, screen_h: int) -> None:
        self.grid_w = len(grid[0])
        self.grid_h = len(grid)
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.side_margin = 10
        self.bottom_margin = 50
        self.top_margin = 10

        self.tile_size: int

    def get_tile_size(self) -> None:
        tile_by_width = ((self.screen_w - self.side_margin * 2) // self.grid_w)
        tile_by_height = ((self.screen_h - self.top_margin - self.bottom_margin)
                          // self.grid_h)
        self.tile_size = min(tile_by_height, tile_by_width)

    def get_offset_x(self) -> int:
        maze_width = self.tile_size * self.grid_w
        unused_width = self.screen_w - maze_width
        offset_x = unused_width // 2
        return offset_x

    def get_offset_y(self) -> int:
        return self.top_margin
