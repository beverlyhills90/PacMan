import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, field_validator


class HighscorePlayer(BaseModel):
    nickname: str = Field(min_length=2, max_length=10)
    score: int = Field(ge=0)

    @field_validator("nickname", mode="before")
    @classmethod
    def nickname_validator(cls, value: str) -> str:
        if len(value) > 10:
            return value[:10]
        return value


class TopTen(BaseModel):
    players: list[HighscorePlayer]

    @classmethod
    def read_top_ten(cls, file_path: Path) -> "TopTen":
        """try exept OSError and jsonDecode"""
        players = []
        with open(file_path) as file:
            data = json.loads(file.read())
        for pl in data:
            try:
                player = HighscorePlayer.model_validate(pl)
                players.append(player)
            except ValidationError:
                continue

        players.sort(key=lambda p: p.score, reverse=True)
        return cls(players=players[:10])

    @staticmethod
    def save(file_path: Path, player_score: int, nickname: str) -> None:
        """try exept OSError and jsonDecode"""
        top = TopTen.read_top_ten(file_path)
        top.players.append(
            HighscorePlayer(nickname=nickname, score=player_score)
        )
        top.players.sort(key=lambda p: p.score, reverse=True)
        with open(file_path, "w") as file:
            data = [p.model_dump() for p in top.players[:10]]
            json.dump(data, file, ensure_ascii=False, indent=4)
