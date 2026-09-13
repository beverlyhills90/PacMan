# PacMan

Tile - src/shared_types.py

build_grid_for_level() -> Grid - public func in maze_adapter.py call it to create maze with tiles
Grid:list[list[Tile]] - grid[row][col] size: (2·height+1) rows * (2·width+1) cols
tile_at(grid, pos:Pos) - helper func to read tile in grid with normal (x,y) coordinates

also i add Exeption Hnadling in parser and potection for highscore_filename: Path agains not str input
