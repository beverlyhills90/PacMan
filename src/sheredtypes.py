from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field


class Level(BaseModel):
    width: Any = Field(default=20)
    height: Any = Field(default=20)
    seed: Any = Field(default=None)


Tile: TypeAlias = Literal["wall", "floor"]
Grid: TypeAlias = list[list[Tile]]
