from typing import cast

from core.player import Player
from core.world import tile_at
from shared_types import Grid

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


def run_frames(p: Player, grid: Grid, actions: list) -> None:
    for i in range(len(actions)):
        p.update(0.25, grid, actions[i])
        check_rules(p, grid)


def check_rules(p: Player, grid: Grid) -> None:
    assert tile_at(grid, p.tile) == "floor"
    if p.direction is None:
        assert p._progress == 0
    assert 0 <= p._progress < 1
    if p.direction is not None:
        assert p.facing == p.direction
    else:
        assert p.facing is not None


def test_player_create() -> None:
    p = Player((1, 1), 2.0)

    assert p._start == (1, 1)
    assert p.tile == (1, 1)
    assert p.direction is None
    assert p.speed == 2.0


def test_player_reset() -> None:
    p = Player((1, 1), 2.0)
    p.tile = (2, 2)
    p.direction = "right"
    p._progress = 0.8
    p.reset()

    assert p.tile == (1, 1)
    assert p.direction is None
    assert p.speed == 2.0
    assert p._progress == 0.0


def test_scree_pos() -> None:
    p = Player((1, 1), 2.0)
    assert p.screen_pos() == (1.0, 1.0)
    p.direction = "right"
    p._progress = 0.25
    p.tile = (3, 1)
    assert p.screen_pos() == (3.25, 1.0)
    p.direction = "up"
    assert p.screen_pos() == (3.0, 0.75)


def test_moves_down_and_stops_at_wall() -> None:
    grid = grid_from(U)
    p = Player((1, 1), 2.0)

    run_frames(p, grid, ["down", None, None, None])
    assert p.tile == (1, 3)
    assert p.direction is None
    check_rules(p, grid)
