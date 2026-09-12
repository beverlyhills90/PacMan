import random
from typing import Any, Literal, TypeAlias, cast

from mazegenerator import MazeGenerator
from pydantic import TypeAdapter, ValidationError

from parcing import Level


class MazeError(Exception):
    def __init__(self, msg="unknown MazeError") -> None:
        super().__init__(msg)


Title: TypeAlias = Literal["wall", "floor"]
Grid: TypeAlias = list[list[Title]]
ta = TypeAdapter(list[list[int]])

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
CLOSED = 15

ALLOWED = [NORTH, EAST, SOUTH, CLOSED]


def build_grid(Level: Level) -> Grid:
    """
    Return 'Grid' TypeAlias = list[list[Title="wall" or "floor"]]
    IT can raise MazeError if maze from MazeGenerator is invalid idk handle it when call
    """
    width: int = Level.width
    height: int = Level.height
    seed: int | None = Level.seed
    raw_maze: list[list[int]] = _generate(width, height, seed=seed)
    validated: list[list[int]] = _validate(raw_maze, width, height)
    return _to_tiles(validated)


def _generate(width: int, height: int, seed: int | None) -> list[list[int]]:
    seed2: Any = seed
    if seed is not None:
        seed2 = random.randint(0, 2**31 - 1)
    maze = MazeGenerator(size=(width, height), seed=seed2)
    maze.generate()
    return maze._maze


def _validate(cells: object, width: int, height: int) -> list[list[int]]:
    try:
        ta.validate_python(cells)
    except Exception:
        raise MazeError("Maze module Generation Error")

    typed_cells = cast(list[list[int]], cells)
    if len(typed_cells) != height:
        raise MazeError("Maze module Generation Error len != height")

    for line, row in enumerate(typed_cells):
        if len(row) != width:
            raise MazeError(
                f"Maze module Generation Error len of ({line}) != width"
            )
        if not all(x for x in row if x in ALLOWED):
            
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
