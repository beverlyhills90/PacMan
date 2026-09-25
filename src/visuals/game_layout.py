from src.shared_types import Grid


class GameLayout:
    """Converts tile positions to pixels and fits the maze in the window.

    Space is left under the maze for the HUD. get_tile_size() must
    be called before the other methods.
    """

    def __init__(self, grid: Grid, screen_w: int, screen_h: int) -> None:
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
        """Compute the largest tile size that fits the maze in the window."""
        tile_by_width = (self.screen_w - self.side_margin * 2) // self.grid_w
        tile_by_height = (
            self.screen_h - self.top_margin - self.bottom_margin
        ) // self.grid_h
        self.tile_size = min(tile_by_height, tile_by_width)
        self.wall_width = int(self.tile_size // 5)

    def get_offset_x(self) -> int:
        """Return the left offset that centres the maze horizontally."""
        maze_width = self.tile_size * self.grid_w
        unused_width = self.screen_w - maze_width
        offset_x = unused_width // 2
        return offset_x

    def get_offset_y(self) -> int:
        """Return the top offset of the maze."""
        return self.top_margin

    def tiles_to_coordinates(
        self, tiles: tuple[float, float]
    ) -> tuple[float, float]:
        """Convert a (possibly fractional) tile position to pixels.

        Returns:
            Top-left pixel coordinates of the tile.
        """
        x_tile, y_tile = tiles
        x = x_tile * self.tile_size + self.get_offset_x()
        y = y_tile * self.tile_size + self.get_offset_y()
        return (x, y)

    def get_hud_coordinates(self) -> tuple[int, int]:
        """Return the position of the first HUD label, below the maze."""
        hud_height = (
            self.screen_h - self.get_offset_y() - (self.tile_size * self.grid_h)
        )
        x = self.get_offset_x() + (self.tile_size // 2)
        y = self.screen_h - (hud_height // 2) - (self.tile_size // 2)
        return (x, y)

    def get_group_width(self, elements_width: list[float], gap: float) -> float:
        """Return the sum of the element widths plus gap."""
        group_width: float = gap
        for element in elements_width:
            group_width += element
        return group_width
