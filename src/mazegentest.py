from typing import Any, Literal, TypeAlias, cast

import mazegenerator

Title: TypeAlias = Literal["wall", "floor"]
Grid: TypeAlias = list[list[Title]]


def _to_tiles(cells: list[list[int]]) -> Grid:
    H = len(cells)
    W: int = len(cells[0])

    grid = [["wall" for _ in range(0,2*W+1)] for _ in range(0, H * 2 + 1)]
    print(len(grid))


if __name__ == "__main__":
    maze = mazegenerator.MazeGenerator(
        size=(20, 20), entry_cell=(0, 0), exit_cell=(3, 2), seed=42
    )
    print(len(maze._maze[0]))
    _to_tiles(maze._maze)
