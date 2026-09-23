from typing import cast

import pytest

from src.core.world import can_move, find_start
from src.shared_types import Direction, Grid, Pos, WorldExeption

U = [
    "#####",
    "#.#.#",
    "#.#.#",
    "#...#",
    "#####",
]

U_large = [
    "#########",
    "#.#.#.#.#",
    "#.#...#.#",
    "#.#.#.#.#",
    "#...#...#",
    "#.#.#.#.#",
    "#.#...#.#",
    "#.#.#.#.#",
    "#########",
]

GRID_WITH_FOOR = [
    "###",
    "#.#",
    "###",
]

GRID_WITHOUT_FOOR = [
    "###",
    "###",
    "###",
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
        ((1, 3), "right", True),
    ],
)
def test_can_move(pos: Pos, direction: Direction, expected: bool) -> None:
    assert can_move(grid_from(U), pos, direction) == expected


def test_find_start() -> None:
    assert find_start(grid_from(U)) == (2,3)
    assert find_start(grid_from(U_large)) == (3, 4)
    assert find_start(grid_from(GRID_WITH_FOOR)) == (1, 1)
    with pytest.raises(WorldExeption):
        assert find_start(grid_from(GRID_WITHOUT_FOOR)) == (1, 1)
