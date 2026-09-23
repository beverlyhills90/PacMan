from collections import deque

from src.shared_types import (
    DELTA,
    Direction,
    Grid,
    Pos,
    Tile,
    WorldException,
)


def place_pacgums(grid: Grid, start: Pos) -> tuple[set[Pos], set[Pos]]:
    super_set: set[Pos] = set()
    left_up_pos = (0, 0)
    right_up_pos = (len(grid[0]), 0)
    left_down_pos = (0, len(grid))
    right_down_pos = (len(grid[0]), len(grid))
    super_set.add(find_target(grid, left_up_pos))
    super_set.add(find_target(grid, right_up_pos))
    super_set.add(find_target(grid, left_down_pos))
    super_set.add(find_target(grid, right_down_pos))
    pacgums = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (col, row) not in super_set and (col, row) != start:
                if grid[row][col] != "wall":
                    pacgums.add((col, row))
    return (pacgums, super_set)


def tile_at(grid: Grid, pos: Pos) -> Tile:
    col, row = pos
    return grid[row][col]


def neighbor(pos: Pos, direction: Direction) -> Pos:
    nc, nr = pos
    dc, dr = DELTA[direction]

    neighbor_x, neighbor_y = nc + dc, nr + dr
    return (neighbor_x, neighbor_y)


def find_start(grid: Grid) -> Pos:
    cc, cr = (len(grid[0]) // 2, len(grid) // 2)
    res = find_target(grid, (cc, cr))
    return res


def can_move(grid: Grid, pos: Pos, direction: Direction) -> bool:
    nc, nr = pos
    dc, dr = DELTA[direction]

    next_move = grid[nr + dr][nc + dc]
    if next_move == "wall":
        return False
    return True


def find_target(grid: Grid, target_pos: Pos) -> Pos:
    cc, cr = target_pos
    if cc < 0:
        cc = 0
    if cc > len(grid[0]) - 1:
        cc = len(grid[0]) - 1
    if cr < 0:
        cr = 0
    if cr > len(grid) - 1:
        cr = len(grid) - 1
    queue = deque([((cc, cr), tile_at(grid, (cc, cr)))])
    visited = {(cc, cr)}

    while len(queue) != 0:
        (mc, mr), current_tile = queue.popleft()
        if current_tile == "floor":
            return (mc, mr)
        else:
            for v in DELTA.values():
                vc, vr = v
                neighbor_col, neighbor_row = (vc + mc, vr + mr)
                if 0 <= neighbor_col < len(grid[0]) and 0 <= neighbor_row < len(
                    grid
                ):
                    if (neighbor_col, neighbor_row) not in visited:
                        queue.append(
                            (
                                (neighbor_col, neighbor_row),
                                tile_at(grid, (neighbor_col, neighbor_row)),
                            )
                        )
                        visited.add((neighbor_col, neighbor_row))

    raise WorldException("No floor tile in maze")
