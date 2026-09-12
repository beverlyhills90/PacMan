from shared_types import DELTA, Direction, Grid, Pos


def find_start(grid: Grid) -> Pos:
    pass


def can_move(grid: Grid, pos: Pos, direction: Direction) -> bool:
    nc, nr = pos
    dc, dr = DELTA[direction]

    next_move = grid[nr + dr][nc + dc]
    if next_move == "wall":
        return False
    return True
