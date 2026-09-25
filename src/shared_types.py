from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field


class Level(BaseModel):
    """One level entry of the config: maze width, height and seed."""

    width: Any = Field(default=20)
    height: Any = Field(default=20)
    seed: Any = Field(default=None)


class WorldException(Exception):
    """Raised when the maze cannot be used to build a level."""

    def __init__(self, msg: str = "Unknown world exception") -> None:
        super().__init__(msg)


class GhostException(WorldException):
    """Raised on an invalid ghost state."""

    def __init__(self, msg: str = "Unknown ghost exception") -> None:
        super().__init__(msg)


Direction = Literal["up", "down", "left", "right"]
GhostMode = Literal["chase", "frightened", "eaten"]
CheatMode = Literal[
    "level_skip",
    "inflives",
    "slow_ghosts",
    "inftime",
    "pluslive",
]
GameStatus = Literal[
    "playing", "level_won", "dead", "game_over", "victory", "countdown", "pause"
]
GhostNames = Literal["blinky", "pinky", "inky", "clyde"]
VisualState = Literal[
    "name_input",
    "menu",
    "start",
    "playing",
    "exit",
    "highscore",
    "victory_screen",
    "controls",
    "lost_screen",
]
Pos = tuple[int, int]  # (col, row)

DELTA: dict[Direction, tuple[int, int]] = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
OPPOSITE: dict[Direction, Direction] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}
Tile: TypeAlias = Literal["wall", "floor"]
Grid: TypeAlias = list[list[Tile]]  # (row, col)


@dataclass(frozen=True)
class PacmanView:
    """Read-only view of Pac-Man for rendering."""

    pos: tuple[float, float]
    facing: Direction
    moving: bool


@dataclass(frozen=True)
class GhostView:
    """Read-only view of one ghost for rendering."""

    name: GhostNames
    pos: tuple[float, float]
    facing: Direction
    mode: GhostMode
    frightened_left: float


@dataclass(frozen=True)
class GameState:
    """Read-only snapshot of the whole game, rendered once per frame."""

    grid: Grid
    player: PacmanView
    ghosts: list[GhostView]
    pacgums: frozenset[Pos]
    super_pacgums: frozenset[Pos]
    score: int
    status: GameStatus
    lives: int
    level: int
    time_left: float
    god_mode: bool
