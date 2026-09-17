import random
from abc import ABC, abstractmethod
from collections import deque
from typing import get_args

from core.world import can_move, find_target, neighbor
from shared_types import (
    DELTA,
    OPPOSITE,
    Direction,
    GhostMode,
    GhsotsNames,
    Grid,
    Pos,
)


class Ghost(ABC):
    def __init__(self, home: Pos, name: GhsotsNames, speed: float) -> None:
        self.home: Pos = home
        self.name: GhsotsNames = name
        self.speed: float = speed
        self.tile: Pos = self.home
        self.direction: Direction = "right"
        self.facing: Direction = "right"
        self._progress: float = 0.0
        self._frightened_left: float = 0.0
        self._respawn_left: float = 0.0
        self.mode: GhostMode = "chase"
        self._rng = random.Random()

    @abstractmethod
    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        pass

    def update(
        self, dt: float, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> None:
        if self.mode == "frightened":
            self._frightened_left -= dt
            if self._frightened_left <= 0.0:
                self.mode = "chase"
        if self.mode == "eaten":
            self._respawn_left -= dt
            if self._respawn_left >= 0.0:
                return
            else:
                self.mode = "chase"
        if self._progress == 0.0:
            self._decide(grid, pacman_tile, pacman_facing)
        self._progress += self.speed * dt
        while self._progress >= 1:
            self.tile = neighbor(self.tile, self.direction)
            self._decide(grid, pacman_tile, pacman_facing)
            self._progress -= 1

    def frighten(self, duration: float) -> None:
        if self.mode == "eaten":
            return
        if self.mode == "frightened":
            self._frightened_left = duration
            return
        self.mode = "frightened"
        self._frightened_left = duration
        if self._progress != 0:
            self.tile = neighbor(self.tile, self.direction)
            self.direction = OPPOSITE[self.direction]
            self.facing = self.direction
            self._progress = 1 - self._progress

    def reset(self) -> None:
        self.tile = self.home
        self.mode = "chase"
        self.direction = "left"
        self.facing = "left"
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
        delta_x, delta_y = DELTA[self.direction]
        res_x = x + delta_x * self._progress
        res_y = y + delta_y * self._progress
        return (res_x, res_y)

    def _current_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        if self.mode == "chase":
            return find_target(
                grid, self.chase_target(grid, pacman_tile, pacman_facing)
            )
        if self.mode == "frightened":
            self_x, self_y = self.tile
            pac_x, pac_y = pacman_tile
            (t_x, t_y) = self_x * 2, self_y * 2
            target_pos = (t_x - pac_x, t_y - pac_y)
            return find_target(grid, target_pos)
        return self.home

    def _choose_direction(self, grid: Grid, target: Pos) -> Direction:
        candidats = []
        for d in get_args(Direction):
            if can_move(grid, self.tile, d) and d != OPPOSITE[self.direction]:
                candidats.append(d)
        if not candidats:
            candidats.append(OPPOSITE[self.direction])
        if self.mode == "frightened":
            return self._rng.choice(candidats)
        if len(candidats) == 1:
            return candidats[0]
        visited = {self.tile}
        q = deque([])
        for d in candidats:
            p = neighbor(self.tile, d)
            if p == target:
                return d
            visited.add(p)
            q.append((p, d))
        while q:
            pos, direct = q.popleft()
            for d, _ in DELTA.items():
                if can_move(grid, pos, d):
                    n = neighbor(pos, d)
                    if n in visited:
                        continue
                    if n == target:
                        return direct
                    else:
                        visited.add(n)
                        q.append((n, direct))
        if self.direction in candidats:
            return self.direction
        else:
            return candidats[0]

    def _decide(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> None:
        target = self._current_target(grid, pacman_tile, pacman_facing)
        self.direction = self._choose_direction(grid, target)
        self.facing = self.direction


class Blinky(Ghost):
    def __init__(
        self,
        home: Pos,
        speed: float,
    ) -> None:
        super().__init__(home, "blinky", speed)

    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        return pacman_tile


class Pinky(Ghost):
    def __init__(self, home: Pos, speed: float) -> None:
        super().__init__(home, "pinky", speed)

    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        pac_x, pac_y = pacman_tile
        delta_x, delta_y = DELTA[pacman_facing]
        target_x = pac_x + (delta_x * 4)
        target_y = pac_y + (delta_y * 4)
        return (target_x, target_y)


class Inky(Ghost):
    def __init__(self, home: Pos, speed: float) -> None:
        super().__init__(home, "inky", speed)

    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        return (0, 1)


class Clyde(Ghost):
    def __init__(self, home: Pos, speed: float) -> None:
        super().__init__(home, "clyde", speed)

    def chase_target(
        self, grid: Grid, pacman_tile: Pos, pacman_facing: Direction
    ) -> Pos:
        return (0, 1)


def new_ghosts(grid: Grid, speed: float) -> list[Ghost]:

    left_up_pos = (0, 0)
    right_up_pos = (len(grid[0]), 0)
    left_down_pos = (0, len(grid))
    right_down_pos = (len(grid[0]), len(grid))
    blinky = Blinky(home=find_target(grid, left_up_pos), speed=speed)
    pinky = Pinky(home=find_target(grid, right_up_pos), speed=speed)
    inky = Inky(home=find_target(grid, left_down_pos), speed=speed)
    clyde = Clyde(home=find_target(grid, right_down_pos), speed=speed)
    return [blinky, pinky, inky, clyde]
