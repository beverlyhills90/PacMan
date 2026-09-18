from pathlib import Path
from .abs_classes import Animation
from .game_layout import GameLayout
import pygame as pg

COUNDOWN_FRAMES_N: int = 8
COUNDOWN_NAMES: list[str] = ["count_1", "count_2", "count_3", "count_go"]


class Countdown(Animation):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        super().__init__(screen, game_layout)
        sprites_path: Path = Path(__file__).resolve().parent / "sprites" / "count"
        self.count_sprites: dict[str, list[pg.Surface]] = {
            name: [pg.transform.scale(
                pg.image.load(f"{sprites_path}/{name}_{frame:02d}.png").convert_alpha(),
                (game_layout.tile_size, game_layout.tile_size))
                for frame in range(COUNDOWN_FRAMES_N)] for name in COUNDOWN_NAMES}

    def draw_countdown(self) -> None:
        pass
