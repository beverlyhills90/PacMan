import random
from typing import Any, cast

from mazegenerator import MazeGenerator

from parsing import Level
from sheredtypes import Grid

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
CLOSED = 15


class MazeError(Exception):
    def __init__(self, msg: str = "unknown MazeError") -> None:
        super().__init__(msg)


def build_grid_for_level(level: Level) -> Grid:
    """
    Return 'Grid' TypeAlias = list[list[Tile="wall" or "floor"]]
    IT can raise MazeError if maze from MazeGenerator is invalid idk handle it when call
    """
    width: int = level.width
    height: int = level.height
    seed: int | None = level.seed
    raw_maze: list[list[int]] = _generate(width, height, seed=seed)
    validated: list[list[int]] = _validate(raw_maze, width, height)
    return _to_tiles(validated)


def _generate(width: int, height: int, seed: int | None) -> list[list[int]]:
    seed2: Any = seed
    if seed is None:
        seed2 = random.randint(1, 2**31 - 1)
    try:
        maze = MazeGenerator(size=(width, height), seed=seed2)
    except Exception as e:
        raise MazeError(f"Maze generator failed: {e}")
    return maze.maze


def _is_list_of_lists_of_ints(obj: object) -> bool:
    if not isinstance(obj, list):
        return False

    return all(
        isinstance(sublist, list) and all(isinstance(x, int) for x in sublist)
        for sublist in obj
    )


def _validate(cells: object, width: int, height: int) -> list[list[int]]:
    if not _is_list_of_lists_of_ints(cells):
        raise MazeError("Maze vlidation Error: Not all clells is digit")

    typed_cells = cast(list[list[int]], cells)
    if len(typed_cells) != height:
        raise MazeError("Maze module Generation Error len != height")

    for line, row in enumerate(typed_cells):
        if len(row) != width:
            raise MazeError(
                f"Maze module Generation Error len of ({line}) != width"
            )
        if not all(0 <= x <= CLOSED for x in row):
            raise MazeError(
                f"Maze module Generation Error row ({line}) contain not allowed mask"
            )

    return typed_cells


def _to_tiles(cells: list[list[int]]) -> Grid:
    H = len(cells)
    W: int = len(cells[0])

    grid = [["wall" for _ in range(0, 2 * W + 1)] for _ in range(0, H * 2 + 1)]
    for y in range(H):
        for x in range(W):
            cell = cells[y][x]
            if cell == CLOSED:
                continue
            grid[2 * y + 1][2 * x + 1] = "floor"
            if cell & EAST == 0:
                grid[2 * y + 1][2 * x + 2] = "floor"
            if cell & SOUTH == 0:
                grid[2 * y + 2][2 * x + 1] = "floor"

    return cast(Grid, grid)
