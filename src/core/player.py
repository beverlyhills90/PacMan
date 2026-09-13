from shared_types import DELTA, Direction, Grid, Pos


class Player:
    def __init__(self, start_pos: Pos, speed: float) -> None:
        self._start: Pos = start_pos  # (col,row)
        self.speed: float = speed  # speed in tiles
        self.direction: Direction | None = None
        self.facing: Direction = "right"
        self._next_direction: Direction | None = None
        self._progress: float = 0.0
        self.tile: Pos = start_pos

    def update(self, dt: float, grid: Grid, intent: Direction | None) -> None:
        if intent is not None:
            self._next_direction = intent
            

    def reset(self) -> None:
        self.tile = self._start
        self.direction = None
        self._next_direction = None
        self._progress = 0.0

    def screen_pos(self) -> tuple[float, float]:
        x, y = self.tile
        if self.direction is None:
            return (float(x), float(y))
        delta_x, delta_y = DELTA[self.direction]
        res_x = x + delta_x * self._progress
        res_y = y + delta_y * self._progress
        return (res_x, res_y)
