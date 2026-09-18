import pygame as pg
from pathlib import Path
from shared_types import Pos

from .buttons import Fonts, MenuButton
from .abs_classes import Animation

FIREWORKS_NAMES = ["cyan", "gold", "pink"]
FIREWORKS_FRAMES_N = 12
FIREWORK_POS: list[Pos] = [(150, 200), (300, 50), (550, 200)]
FIREWORK_DELAY: list[float] = [0, 500, 1000]


class Fireworks(Animation):
    def __init__(self, screen: pg.Surface, name: str, delay: float, pos: Pos) -> None:
        super().__init__(screen)
        sprite_path = Path(__file__).resolve().parent / "sprites" / "fireworks"
        self.firework_sprites: list[pg.Surface] = [pg.image.load(
            f"{sprite_path}/firework_{name}_{frame:02d}.png").convert_alpha()
            for frame in range(FIREWORKS_FRAMES_N)]
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
            self.update_frame(frames, FIREWORKS_FRAMES_N, False)
            if self.current_frame in range(FIREWORKS_FRAMES_N):
                self.screen.blit(self.firework_sprites[self.current_frame], self.pos)


class VictoryView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.button_list: list[MenuButton] = self.create_buttons()
        self.victory_surface: pg.Surface = pg.Surface((screen.width, screen.height), pg.SRCALPHA)
        self.fireworks: dict[str, Fireworks] = {
            name: Fireworks(screen, name, delay, pos)
            for name, delay, pos in zip(FIREWORKS_NAMES, FIREWORK_DELAY, FIREWORK_POS)}

    def draw_victory(self, mouse_pos: tuple[int, int], dt: float) -> None:
        self.victory_surface.fill((0, 0, 0, 170))
        self.screen.blit(self.victory_surface)
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos, False)
        for firework in FIREWORKS_NAMES:
            self.fireworks[firework].draw_firework(dt)

    def create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        button = MenuButton((400, 200), "YOU  WON", None, self.fonts.big_button_font,
                            self.fonts.big_button_hover_font)
        button_list.append(button)
        button = MenuButton((400, 300), "YOUR SCORE", None, self.fonts.mid_button_font,
                            self.fonts.mid_button_hover_font)
        button_list.append(button)
        button = MenuButton((400, 400), "PRESS ANY KEY TO PLAY", None, self.fonts.small_button_font,
                            self.fonts.small_button_hover_font)
        button_list.append(button)
        return button_list
