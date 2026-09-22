import math

from core.ghosts import Ghost, new_ghosts
from core.maze_adapter import build_grid_for_level
from core.player import Player, new_player
from core.world import place_pacgums
from parsing import Config
from shared_types import (
    CheatMode,
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
        speed: float = 8,
    ) -> None:
        self.speed: float = speed
        self.ghosts_speed = speed
        self.config: Config = config
        self.level_index: int = 0
        self.level_grid: Grid = build_grid_for_level(self.config.levels[0])
        self.player: Player = new_player(self.level_grid, speed)
        self.ghosts: list[Ghost] = new_ghosts(self.level_grid, speed)
        pacgums, super_pacgums = place_pacgums(
            self.level_grid, self.player.tile
        )
        self.cheat_buf: dict[CheatMode, bool] = {
            "inftime": False,
            "inflives": False,
            "slow_ghosts": False,
        }
        self.pacgums: set[Pos] = pacgums
        self.super_pacgums = super_pacgums
        self.score: int = 0
        self.lives: int = self.config.lives
        self.time_left: float = float(self.config.level_max_time)
        self.status: GameStatus = "countdown"
        self.SCORES_CONST = {
            "Ghost": self.config.points_per_ghost,
            "PucGum": self.config.points_per_pacgum,
            "SuperPacGum": self.config.points_per_super_pacgum,
        }

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

    def cheat(self, code: CheatMode) -> None:
        if code == "inflives":
            self.cheat_buf["inflives"] = not self.cheat_buf["inflives"]
        if code == "inftime":
            self.cheat_buf["inftime"] = not self.cheat_buf["inftime"]
        if code == "slow_ghosts":
            self._slow_ghost()
        if code == "level_skip":
            if self.status == "playing":
                self.status = "level_won"
        if code == "pluslive":
            self.lives += 1

    def _tick_timer(self, dt: float) -> None:
        if not self.cheat_buf["inftime"]:
            self.time_left -= dt
        if self.time_left <= 0:
            self.status = "game_over"

    def _start_level(self, index: int) -> None:
        self.level_grid = build_grid_for_level(level=self.config.levels[index])
        self.player = new_player(self.level_grid, self.speed)
        self.ghosts = new_ghosts(self.level_grid, self.ghosts_speed)
        pacgums, super_pacgums = place_pacgums(
            self.level_grid, self.player.tile
        )
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums
        self.time_left = self.config.level_max_time

    def _eat_pacgum(self) -> None:
        if self.player.tile in self.pacgums:
            self.pacgums.remove(self.player.tile)
            self.score += self.SCORES_CONST["PucGum"]
        if self.player.tile in self.super_pacgums:
            self.super_pacgums.remove(self.player.tile)
            self.score += self.SCORES_CONST["SuperPacGum"]
            for g in self.ghosts:
                g.frighten(3.5)

    def respawn(self) -> None:
        if self.status != "dead":
            return
        if self.lives <= 0:
            return
        self.player.reset()
        for g in self.ghosts:
            g.reset()
        self.status = "countdown"

    def _check_collisions(self) -> None:
        for g in self.ghosts:
            if math.dist(self.player.screen_pos(), g.screen_pos()) < 0.5:
                if g.mode == "frightened":
                    g.eat(respawn_left=3)
                    self.score += self.SCORES_CONST["Ghost"]
                elif g.mode == "eaten":
                    continue
                else:
                    if not self.cheat_buf["inflives"]:
                        self._die()
                    return

    def _check_level_end(self) -> None:
        if len(self.pacgums) == 0:
            self.status = "level_won"

    def next_level(self) -> None:
        if self.level_index == len(self.config.levels) - 1:
            self.status = "victory"
            return
        self.level_index += 1
        self._start_level(self.level_index)
        self.status = "countdown"

    def end_countdown(self) -> None:
        if self.status == "countdown":
            self.status = "playing"

    def _die(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.status = "game_over"
        else:
            self.status = "dead"

    def _slow_ghost(self) -> None:
        self.cheat_buf["slow_ghosts"] = not self.cheat_buf["slow_ghosts"]
        if self.cheat_buf["slow_ghosts"]:
            self.ghosts_speed = 0.2
        else:
            self.ghosts_speed = self.speed
        for g in self.ghosts:
            g.speed = self.ghosts_speed
