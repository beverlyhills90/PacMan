from core.world import can_move, neighbor
from shared_types import DELTA, OPPOSITE, Direction, Grid, Pos


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
        """
        Update player pos and facing
        dt = delta time
        grid = grid
        intend = handled direction

        return None
        no raise
        """
        if intent is not None:
            self._next_direction = intent
        if (
            self._next_direction is not None
            and OPPOSITE[self._next_direction] == self.direction
        ):
            self.tile = neighbor(self.tile, self.direction)
            self.direction = self._next_direction
            self.facing = self.direction
            self._progress = 1 - self._progress
        if self.direction is None:
            if self._next_direction is not None and can_move(
                grid, self.tile, self._next_direction
            ):
                self.facing = self._next_direction
                self.direction = self._next_direction
            elif self._next_direction is not None and intent is not None:
                self.facing = intent
                return
            else:
                return
        self._progress += self.speed * dt
        while self._progress >= 1:
            if self.direction is None:
                break
            self.tile = neighbor(self.tile, self.direction)
            self._progress -= 1
            if self._next_direction is not None and can_move(
                grid, self.tile, self._next_direction
            ):
                self.direction = self._next_direction
                self.facing = self.direction
            if not can_move(grid, self.tile, self.direction):
                self.direction = None
                self._progress = 0

    def reset(self) -> None:
        self.tile = self._start
        self.direction = None
        self._next_direction = None
        self._progress = 0.0

    def screen_pos(self) -> tuple[float, float]:
        """return (x,y) for screen pos"""

        x, y = self.tile
        if self.direction is None:
            return (float(x), float(y))
        delta_x, delta_y = DELTA[self.direction]
        res_x = x + delta_x * self._progress
        res_y = y + delta_y * self._progress
        return (res_x, res_y)
