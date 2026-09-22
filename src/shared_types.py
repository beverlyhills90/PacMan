from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field


class Level(BaseModel):
    width: Any = Field(default=20)
    height: Any = Field(default=20)
    seed: Any = Field(default=None)


class WorldExeption(Exception):
    def __init__(self, msg: str = "Unkonwn World Exeption") -> None:
        super().__init__(msg)


class GhostExeption(WorldExeption):
    def __init__(self, msg: str = "Unkonwn Ghost Exeption") -> None:
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
GhsotsNames = Literal["blinky", "pinky", "inky", "clyde"]
VisualState = Literal["menu", "start", "playing", "exit", "highscore", "victory_screen"]
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
    pos: tuple[float, float]
    facing: Direction
    moving: bool


@dataclass(frozen=True)
class GhostView:
    name: GhsotsNames
    pos: tuple[float, float]
    facing: Direction
    mode: GhostMode
    frightened_left: float


@dataclass(frozen=True)
class GameState:
    grid: Grid
    player: PacmanView
    ghosts: list[GhostView]
    pacgums: frozenset[Pos]
    super_pacgums: frozenset[Pos]
    score: int
    status: GameStatus
    lives: int
    level: int
