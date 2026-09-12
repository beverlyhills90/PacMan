from shared_types import Direction, Grid, Pos, Tile


class Player:
    def __init__(self, start: Pos, speed: float) -> None:
        self.start: Pos = start  # (col,row)
        self.speed: float = speed  # speed in tiles
        self.direction: Direction | None = None
        self.facing: Direction = "right"
        self._next_direction: Direction = "right"
        self.progress: float = 0.0
        self.tile: Pos = start

    def update(self, dt: float, grid: Grid, intent: Direction | None) -> None:
        pass

    def reset(self) -> None:
        pass

    def screen_pos(self) -> tuple[float, float]:
        pass
