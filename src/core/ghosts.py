from abc import ABC, abstractmethod

from core.world import can_move, find_target, neighbor, tile_at
from shared_types import DELTA, Direction, GhostMode, Grid, Pos


class Ghost(ABC):
    def __init__(self, home: Pos, name: str, speed: float) -> None:
        super().__init__()
        self.home: Pos = home
        self.name: str = name
        self.speed: float = speed
        self.tile: Pos = self.home
        self.direction: Direction = "right"
        self.facing: Direction = "right"
        self._progress: float = 0.0
        self._frightened_left: float = 0.0
        self._respawn_left: float = 0.0
        self.mode: GhostMode = "chase"

    @abstractmethod
    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        pass

    def update(
        self, dt: float, grid: Grid, target: Pos, pacman_facing: Direction
    ) -> None:
        if self.mode == "frightened":
            self._frightened_left -= dt
            if self._frightened_left <= 0.0:
                self.mode = "chase"
        if self.mode == "eaten":
            self._respawn_left -= dt
            if self._respawn_left >= 0.0:
                return
        if self._progress == 0.0:
            self.direction = self._choose_direction(grid, target, pacman_facing)
            self.facing = self.direction
        self._progress += self.speed * dt
        while self._progress >= 1:
            self.tile = neighbor(self.tile, self.direction)
            self.direction = self._choose_direction(grid, target, pacman_facing)
            self.facing = self.direction
            self._progress -= 1
            if self.mode == "eaten" and self.tile == self.home:
                self.direction = "right"
                self.facing = self.direction

    def frighten(self, duration: float) -> None: ...

    def reset(self) -> None:
        self.tile = self.home
        self.mode = "chase"
        self.direction = "right"
        self._progress = 0.0
        self._frightened_left = 0.0
        self._respawn_left = 0.0

    def eat(self, respawn_left: float) -> None:
        """if ghost was eaten"""
        self.reset()
        self._respawn_left = respawn_left
        self.mode = "eaten"

    def screen_pos(self) -> tuple[float, float]:
        x, y = self.tile
        if self.direction is None:
            return (float(x), float(y))
        delta_x, delta_y = DELTA[self.direction]
        res_x = x + delta_x * self._progress
        res_y = y + delta_y * self._progress
        return (res_x, res_y)

    def _current_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        pass

    def _choose_direction(
        self, grid: Grid, target: Pos, pacman_facing: Direction
    ) -> Direction:
        pass


class Blinky(Ghost):
    def __init__(
        self,
        home: Pos,
        speed: float = 2.0,
    ) -> None:
        super().__init__(home, "blinky", speed)
