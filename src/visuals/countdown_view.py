from pathlib import Path
from .abs_classes import Animation
from src.game import Game
import pygame as pg

COUNDOWN_FRAMES_N: int = 8
COUNDOWN_NAMES: list[str] = ["count_3", "count_2", "count_1", "count_go"]
COUNDOWN_SEQUENCY = (0, 1, 2, 3, 4, 5, 6, 7)


class Countdown(Animation):
    def __init__(self, screen: pg.Surface, game: Game) -> None:
        super().__init__(screen)
        self.game = game
        sprites_path: Path = Path(__file__).resolve().parent / "sprites" / "count"
        self.count_sprites: dict[str, list[pg.Surface]] = {
            name: [
                pg.image.load(f"{sprites_path}/{name}_{frame:02d}.png").convert_alpha()
                for frame in range(COUNDOWN_FRAMES_N)] for name in COUNDOWN_NAMES}
        self.count_rect = self.count_sprites["count_1"][0].get_rect(
            center=self.screen.get_rect().center)
        self.total_time_ellapsed: float = 0

    def draw_countdown(self, dt: float) -> None:
        self.update_time(dt)
        cur_count = self.update_count(dt)
        if not cur_count:
            return
        frame = 0
        while self.animation_elapsed >= 125:
            frame += 1
            self.animation_elapsed -= 125
        self.update_frame(frame, COUNDOWN_SEQUENCY)
        # print(self.current_frame)
        sprite = self.count_sprites[cur_count][self.current_frame]
        self.screen.blit(sprite, self.count_rect)

    def update_count(self, dt: float) -> str | None:
        self.total_time_ellapsed += dt * 1000
        if self.total_time_ellapsed >= 4000:
            self.game.end_countdown()
            return None
        cur_number = self.total_time_ellapsed // 1000
        return COUNDOWN_NAMES[int(cur_number)]

    def reset_animation(self) -> None:
        self.current_frame = 0
        self.total_time_ellapsed = 0
        self.animation_elapsed = 0
