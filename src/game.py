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

SCORES_CONST = {"Ghost": 400, "PucGum": 50, "SuperPacGum": 100}


class Game:
    def __init__(
        self,
        config: Config,
        lives: int = 3,
        speed: float = 8,
    ) -> None:
        self.speed = speed
        self.config: Config = config
        self.level_index: int = 0
        self.level_grid: Grid = build_grid_for_level(self.config.levels[0])
        self.player: Player = new_player(self.level_grid, speed)
        self.ghosts: list[Ghost] = new_ghosts(self.level_grid, speed)
        pacgums, super_pacgums = place_pacgums(
            self.level_grid, self.player.tile
        )
        self.pacgums: set[Pos] = pacgums
        self.super_pacgums = super_pacgums
        self.score: int = 0
        self.lives: int = lives
        self.time_left: float = float(self.config.level_max_time)
        self.status: GameStatus = "countdown"
        self.transition_left = 1

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
            self.level_index + 1,
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
        pacgums, super_pacgums = place_pacgums(
            self.level_grid, self.player.tile
        )
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums
        self.time_left = self.config.level_max_time

    def _eat_pacgum(self) -> None:
        if self.player.tile in self.pacgums:
            self.pacgums.remove(self.player.tile)
        if self.player.tile in self.super_pacgums:
            self.super_pacgums.remove(self.player.tile)
            for g in self.ghosts:
                g.frighten(3.5)

    def _respawn(self) -> None:
        if self.lives <= 0:
            return
        self.player.reset()
        for g in self.ghosts:
            g.reset()

    def _check_collisions(self) -> None:
        for g in self.ghosts:
            if self.player.tile == g.tile:
                if g.mode == "frightened":
                    g.eat(respawn_left=2)
                else:
                    self._die()

    def _check_level_end(self) -> None:
        if len(self.pacgums) == 0:
            self.status = "level_won"
            self.transition_left = 1

    def next_level(self) -> None:
        if self.level_index == len(self.config.levels) - 1:
            self.status = "victory"
            return
        self.level_index += 1
        self._start_level(self.level_index)
        self.status = "playing"

    def _die(self):
        self.lives -= 1
        if self.lives <= 0:
            self.status = "game_over"
        else:
            self.status = "dead"
            self.transition_left = 1

    def _eat_at(self, tile: Pos) -> None:
        pass
