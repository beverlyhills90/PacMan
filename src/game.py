from core.ghosts import Ghost, new_ghosts
from core.maze_adapter import build_grid_for_level
from core.player import Player, new_player
from core.world import place_pacgums
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
        super_pacgums: set[Pos],
        lives: int,
        time_left: int = 90,
        speed: float = 8,
    ) -> None:
        self.speed = speed
        self.config: Config = config
        self.level_index: int = 0
        self.level_grid: Grid = level_grid
        self.player: Player = new_player(self.level_grid, speed)
        self.ghosts: list[Ghost] = new_ghosts(self.level_grid, speed)
        self.pacgums: set[Pos] = set([(1, 0)])
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
        self._eat_pacgum()

        for g in self.ghosts:
            g.update(dt, self.level_grid, self.player.tile, self.player.facing)
        self._check_collisions()
        self._check_level_end()
        if self.status == "level_won":
            self._next_level()
        if self.status == "victory":
            return

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
        self.level_grid = build_grid_for_level(level=self.config.levels[index])
        self.player = new_player(self.level_grid, self.speed)
        self.ghosts = new_ghosts(self.level_grid, self.speed)
        self.pacgums = set([(10, 10)])

    def _eat_pacgum(self) -> None:
        if self.time_left <= 80:
            self.pacgums.pop()

    def _respawn(self) -> None:
        if self.lives <= 0:
            return
        self.player.reset()
        for g in self.ghosts:
            g.mode = "chase"
        self.lives -= 1

    def _check_collisions(self) -> None:
        pass

    def _check_level_end(self) -> None:
        if len(self.pacgums) == 0:
            self.status = "level_won"

    def _next_level(self) -> None:
        if self.level_index <= len(self.config.levels):
            self.status = "victory"
            return
        self.level_index += 1
        self._start_level(self.level_index)

    def _eat_at(self, tile: Pos) -> None:
        pass
