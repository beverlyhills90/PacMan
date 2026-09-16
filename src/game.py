from core.ghosts import Blinky, Clyde, Ghost, Inky, Pinky
from core.player import Player
from core.world import new_ghosts, new_player
from parsing import Config
from shared_types import (
    Direction,
    GameState,
    GameStatus,
    GhostView,
    Grid,
    PacmanView,
    Pos,
)


class Game:
    def __init__(
        self,
        config: Config,
        level_grid: Grid,
        pacgums: set[Pos],
        super_pacgums: set[Pos],
        lives: int,
        time_left: int = 90,
        speed: float = 8,
    ) -> None:
        self.config: Config = config
        self.level_index: int = 0
        self.level_grid: Grid = level_grid
        self.player: Player = new_player(self.level_grid, speed)
        self.ghosts: list[Ghost] = new_ghosts(self.level_grid, speed)
        self.pacgums: set[Pos] = pacgums
        self.super_pacgums = super_pacgums
        self.score: int = 0
        self.lives: int = lives
        self.time_left: float = float(time_left)
        self.status: GameStatus = "playing"

    def update(self, dt: float, intent: Direction | None) -> None:
        if self.status != "playing":
            return
        self._tick_timer(dt)
        self.player.update(dt, self.level_grid, intent)
        self._eat_pucgum()

        for g in self.ghosts:
            pass
        self._check_collisions()
        self._check_level_end()

    def snapshot(self) -> GameState:
        player_moving = True
        if self.player.direction is None:
            player_moving = False
        pacman_view = PacmanView(
            pos=self.player.screen_pos(),
            facing=self.player.facing,
            moving=player_moving,
        )
        ghost_views = []
        for g in self.ghosts:
            ghost_views.append(
                GhostView(
                    g.name, g.screen_pos(), g.facing, g.mode, g._frightened_left
                )
            )
        game_state = GameState(
            self.level_grid,
            pacman_view,
            ghost_views,
            frozenset(self.pacgums),
            frozenset(self.super_pacgums),
            self.score,
            self.status,
            self.lives,
            self.level_index,
        )
        return game_state

    def cheat(self, code: str) -> None:
        pass

    def _tick_timer(self, dt: float) -> None:
        self.time_left -= dt
        if self.time_left <= 0:
            self.status = "game_over"

    def _start_level(self, index: int) -> None:
        pass

    def _eat_pucgum(self) -> None:
        pass

    def _respawn(self) -> None:
        pass

    def _check_collisions(self) -> None:
        pass

    def _check_level_end(self) -> None:
        pass

    def _next_level(self) -> None:
        pass

    def _eat_at(self, tile: Pos) -> None:
        pass
