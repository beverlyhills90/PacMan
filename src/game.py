import math
import sys
from json import JSONDecodeError

from src.core.ghosts import Ghost, new_ghosts
from src.core.maze_adapter import build_grid_for_level
from src.core.player import Player, new_player
from src.core.sound import Sounds
from src.core.world import place_pacgums
from src.highscore import TopTen
from src.parsing import Config
from src.shared_types import (
    CheatMode,
    Direction,
    GameState,
    GameStatus,
    GhostView,
    Grid,
    PacmanView,
    Pos,
)

DIFFICULTY_LEVEL = {1: 0.5, 2: 0.7, 3: 0.9}


class Game:
    """Rules and state machine of a single play session.

    The engine owns the maze, the player, the ghosts and the score, and
    exposes its state to the presentation layer through `snapshot()`.
    It never imports a graphical library, so it can run headless.
    """

    def __init__(
        self,
        config: Config,
        nickname: str,
        speed: float = 8,
    ) -> None:
        """Build the first level and put the game in the countdown state.

        Args:
            config: Validated configuration (lives, points, levels, ...).
            nickname: Player name stored with the score in the top ten.
            speed: Pac-Man speed in tiles per second; ghost speed is
                derived from it through the configured difficulty level.
        """
        self.config: Config = config
        self.speed: float = speed
        self.ghosts_speed = (
            speed * DIFFICULTY_LEVEL[self.config.difficulty_level]
        )
        self.level_index: int = 0
        self.level_grid: Grid = build_grid_for_level(self.config.levels[0])
        self.player: Player = new_player(self.level_grid, speed)
        self.ghosts: list[Ghost] = new_ghosts(
            self.level_grid,
            self.ghosts_speed,
        )
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
        self.points = {
            "Ghost": self.config.points_per_ghost,
            "PacGum": self.config.points_per_pacgum,
            "SuperPacGum": self.config.points_per_super_pacgum,
        }
        self.prev_status: GameStatus = self.status
        self.nickname: str = nickname
        self.sounds = Sounds()

    def update(self, dt: float, intent: Direction | None) -> None:
        """Advance the game by one frame.

        Does nothing unless the status is "playing", so pauses, the start
        countdown and the end-of-game states freeze the world without any
        extra handling on the caller side.

        Args:
            dt: Seconds elapsed since the previous frame.
            intent: Direction requested by the player this frame, or None.
        """
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
        """Return an immutable view of the current state for rendering.

        Sets are copied into frozensets, so the caller cannot modify the
        game by holding on to the result.

        Returns:
            The state of this frame: maze, entities, pacgums, score,
            lives, level number, remaining time and status.
        """
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
            round(self.time_left),
            self.cheat_buf["inflives"],
        )
        return game_state

    def cheat(self, code: CheatMode) -> None:
        """Apply a cheat requested by the reviewer.

        "inflives", "inftime" and "slow_ghosts" are toggles and can be
        switched off by sending the same code again; "level_skip" and
        "pluslive" act once. "level_skip" is ignored unless a level is
        actually running.

        Args:
            code: Cheat identifier bound to a key by the input layer.
        """
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
            self.sounds.play_sound("eat_pac_gum")
            self.score += self.points["PacGum"]
        if self.player.tile in self.super_pacgums:
            self.super_pacgums.remove(self.player.tile)
            self.score += self.points["SuperPacGum"]
            for g in self.ghosts:
                g.frighten(4)

    def respawn(self) -> None:
        """Put Pac-Man and the ghosts back on their starting tiles.

        Called by the presentation layer once the death animation is
        over. Eaten pacgums and the score are kept, so the player
        continues the same level. Does nothing unless the player is
        dead and still has lives left; the next state is the countdown.
        """
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
                    self.sounds.play_sound("eat_ghost")
                    self.score += self.points["Ghost"]
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
        """Move on to the next level, or finish the game.

        Called by the presentation layer when it has finished showing the
        "level won" screen. On the last level the status becomes
        "victory" and the score is written to the highscore file; a
        failure to write is reported on stderr and never raises.
        Otherwise a fresh level is built and the countdown starts again.
        """
        if self.level_index == len(self.config.levels) - 1:
            self.status = "victory"
            self.sounds.play_sound("victory")
            try:
                TopTen.save(
                    self.config.highscore_filename, self.score, self.nickname
                )
            except OSError as e:
                print(f"[Error] saving {e.errno} {e}", file=sys.stderr)
            except JSONDecodeError as e:
                print(f"[Error] saving {e.msg}", file=sys.stderr)
            return
        self.level_index += 1
        self._start_level(self.level_index)
        self.status = "countdown"

    def end_countdown(self) -> None:
        """Start playing once the countdown animation has finished.

        Ignored in any other status, so a view that keeps calling it
        cannot resurrect a finished or paused game.
        """
        if self.status == "countdown":
            self.status = "playing"

    def _die(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.status = "game_over"
        else:
            self.status = "dead"
            self.sounds.play_sound("game_lost")

    def _slow_ghost(self) -> None:
        self.cheat_buf["slow_ghosts"] = not self.cheat_buf["slow_ghosts"]
        if self.cheat_buf["slow_ghosts"]:
            self.ghosts_speed = 0.2
        else:
            self.ghosts_speed = self.speed
        for g in self.ghosts:
            g.speed = self.ghosts_speed

    def pause(self) -> None:
        """Toggle the pause.

        Pausing remembers the current status and replaces it with
        "pause", which freezes `update()`; unpausing restores the
        remembered status, so a pause during the countdown resumes into
        the countdown rather than straight into play.
        """
        if self.status != "pause":
            self.prev_status = self.status
            self.status = "pause"
        else:
            self.status = self.prev_status
