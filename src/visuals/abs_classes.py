from abc import ABC
from pathlib import Path

import pygame as pg

SCORE_DIST = 32

DIGIT_FRAMES: int = 4
DIGIT_SEQUENCE = (0, 1, 2, 3, 2, 1)
DIGIT_FRAME_DUR = 180


class Animation(ABC):
    """Base class for sprite animations: a frame index and a clock."""
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, step: int, sequence: tuple[int, ...] | None) -> None:
        """Advance the animation by step frames.

        Args:
            step: Number of frames to advance.
            sequence: Frame order to loop through; if None, the frame
                index just grows.
        """
        if sequence:
            self.current_frame = sequence[
                (self.current_frame + step) % len(sequence)
            ]
        else:
            self.current_frame = self.current_frame + step

    def update_time(self, dt: float) -> None:
        """Add dt seconds to the animation clock (stored in ms)."""
        self.animation_elapsed = self.animation_elapsed + dt * 1000


def get_centered_x(name_width: float, screen_width: int) -> float:
    """Return the x at which a name and a 6-digit score are centred.

    Args:
        name_width: Width of the rendered name in pixels.
        screen_width: Width of the screen in pixels.

    Returns:
        Left x coordinate of the name.
    """
    total_width = name_width + SCORE_DIST + 32 * 6
    left_width = screen_width - total_width
    return left_width // 2


class Highscore(Animation):
    """Draws a score with animated digit sprites."""
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__(screen)
        main_path = Path(__file__).resolve().parent / "sprites" / "highscore_32"
        self.digit_sprites: dict[str, list[pg.Surface]] = {
            str(name): [
                pg.image.load(
                    f"{main_path}/digit_{name}_{frame}.png"
                ).convert_alpha()
                for frame in range(DIGIT_FRAMES)
            ]
            for name in range(10)
        }

        self.center_y = self.digit_sprites["1"][0].get_rect().centery

    def draw_highscore(self, score: int, dt: float, x: float, y: float) -> None:
        """Draw the score as 6 animated digits, zero-padded.

        Args:
            score: Score to draw.
            dt: Seconds elapsed since the previous frame.
            x: Left x of the first digit.
            y: Bottom y of the digits.
        """
        self.update_time(dt)
        frames = 0
        while self.animation_elapsed >= DIGIT_FRAME_DUR:
            self.animation_elapsed -= DIGIT_FRAME_DUR
            frames += 1
        self.update_frame(frames, DIGIT_SEQUENCE)
        normalised_score = self.normalise_score(score)
        number = normalised_score.zfill(6)
        for index, digit in enumerate(number):
            sprite = self.digit_sprites[digit][self.current_frame]
            sprite_rect = sprite.get_rect(bottomleft=(x + 24 * index, y))
            self.screen.blit(sprite, sprite_rect)

    def normalise_score(self, score: int) -> str:
        """Return the score as a string, capped at 999999."""
        while score > 999999:
            return str(999999)
        return str(score)
