from typing import cast

import pytest

from core.world import can_move
from shared_types import Direction, Grid, Pos

U = [
    "#####",
    "#.#.#",
    "#.#.#",
    "#...#",
    "#####",
]


def grid_from(u: list[str]) -> Grid:
    grid = [["wall" for _ in range(len(row))] for row in u]
    for r in range(len(u)):
        for c in range(len(grid[r])):
            if u[r][c] == ".":
                grid[r][c] = "floor"
    return cast(Grid, grid)


@pytest.mark.parametrize(
    ("pos", "direction", "expected"),
    [
        ((1, 1), "up", False),
        ((1, 1), "down", True),
        ((1, 1), "left", False),
        ((2, 2), "right", True),
    ],
)
def test_can_move(pos: Pos, direction: Direction, expected: bool) -> None:
    assert can_move(grid_from(U), pos, direction) == expected
