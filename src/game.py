from core.ghosts import Ghost
from core.player import Player
from parsing import Config
from shared_types import Direction, GameStatus, Grid, Pos


class Game:
    def __init__(
        self,
        config: Config,
        level_grid: Grid,
        player: Player,
        ghosts: list[Ghost],
        pacgums: set[Pos],
        super_pacgums: set[Pos],
        lives: int,
        time_left: int = 90,
    ) -> None:
        self.config: Config = config
        self.level_index: int = 0
        self.leve_grid: Grid = level_grid
        self.player: Player = player
        self.ghosts: list[Ghost] = ghosts
        self.pacgums: set[Pos] = pacgums
        self.score: int = 0
        self.lives: int = lives
        self.time_left: float = float(time_left)
        self.status: GameStatus = "playing"

    def update(self, dt: float, intent: Direction | None) -> None: ...
    def snapshot(self) -> GameState: ...
    def cheat(self, code: str) -> None: ...
    def _start_level(self, index: int) -> None: ...
    def _respawn(self) -> None: ...
    def _next_level(self) -> None: ...
    def _eat_at(self, tile: Pos) -> None: ...
