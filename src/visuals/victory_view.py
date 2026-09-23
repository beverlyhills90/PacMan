from pathlib import Path

import pygame as pg

from src.shared_types import Pos

from .abs_classes import Animation, Highscore, get_centered_x
from .buttons import Fonts, MenuButton

FIREWORKS_NAMES = ["cyan", "gold", "pink"]
FIREWORKS_FRAMES_N = 12
FIREWORK_POS: list[Pos] = [(100, 200), (300, 50), (550, 200)]
FIREWORK_DELAY: list[float] = [0, 500, 1000]


DIGIT_FRAMES: int = 4
DIGIT_SEQUENCE = (0, 1, 2, 3, 2, 1)
DIGIT_FRAME_DUR = 180


class Fireworks(Animation):
    def __init__(
        self, screen: pg.Surface, name: str, delay: float, pos: Pos
    ) -> None:
        super().__init__(screen)
        sprite_path = Path(__file__).resolve().parent / "sprites" / "fireworks"
        self.firework_sprites: list[pg.Surface] = [
            pg.image.load(
                f"{sprite_path}/firework_{name}_{frame:02d}.png"
            ).convert_alpha()
            for frame in range(FIREWORKS_FRAMES_N)
        ]
        self.delay: float = delay
        self.local_elapsed: float = 0
        self.pos: Pos = pos

    def draw_firework(self, dt: float) -> None:
        self.local_elapsed += dt * 1000
        if self.local_elapsed >= self.delay:
            self.update_time(dt)
            frames = 0
            while self.animation_elapsed >= 90:
                frames += 1
                self.animation_elapsed -= 90
            self.update_frame(frames, None)
            if self.current_frame in range(FIREWORKS_FRAMES_N):
                self.screen.blit(
                    self.firework_sprites[self.current_frame], self.pos
                )


class VictoryView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.victory_button_list: list[MenuButton] = self.create_buttons()
        self.lost_button_list: list[MenuButton] = self.create_buttons(True)
        self.victory_surface: pg.Surface = pg.Surface(
            (screen.width, screen.height), pg.SRCALPHA
        )
        self.fireworks: dict[str, Fireworks] = {
            name: Fireworks(screen, name, delay, pos)
            for name, delay, pos in zip(
                FIREWORKS_NAMES, FIREWORK_DELAY, FIREWORK_POS
            )
        }
        self.highscore = Highscore(screen)
        self.score_x: float
        self.score_y: float

    def draw_victory(self, mouse_pos: tuple[int, int], dt: float, lost: bool = False) -> None:
        self.victory_surface.fill((0, 0, 0, 170))
        self.screen.blit(self.victory_surface)
        if lost is False:
            for button in self.victory_button_list:
                button.draw_button(self.screen, mouse_pos, False)
            for firework in FIREWORKS_NAMES:
                self.fireworks[firework].draw_firework(dt)
        else:
            for button in self.lost_button_list:
                button.draw_button(self.screen, mouse_pos, False)
        self.highscore.draw_highscore(777, dt, self.score_x, self.score_y)

    def create_buttons(self, lost: bool = False) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        if lost is True:
            button = MenuButton(
                (400, 200),
                "YOU  LOST",
                None,
                self.fonts.big_button_font,
                self.fonts.big_button_hover_font,
            )
            button_list.append(button)
        else:
            button = MenuButton(
                (400, 200),
                "YOU  WON",
                None,
                self.fonts.big_button_font,
                self.fonts.big_button_hover_font,
            )
            button_list.append(button)
        score_rect = self.fonts.mid_button_font.render(
            "YOUR SCORE", False, "white"
        ).get_rect()
        x = get_centered_x(score_rect.width, self.screen.width)
        button = MenuButton(
            (x + score_rect.width // 2, 300),
            "YOUR SCORE",
            None,
            self.fonts.mid_button_font,
            self.fonts.mid_button_hover_font,
        )
        self.score_x = x + score_rect.width
        self.score_y = 300 + score_rect.height // 2
        button_list.append(button)
        button = MenuButton(
            (400, 400),
            "PRESS ANY KEY TO PLAY",
            None,
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(button)
        return button_list
