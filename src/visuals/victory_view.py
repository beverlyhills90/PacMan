import pygame as pg
from pathlib import Path
from shared_types import Pos

from .buttons import Fonts, MenuButton
from .game_layout import GameLayout
from .abs_classes import Animation

FIREWORKS_NAMES = ["cyan", "gold", "pink"]
FIREWORKS_FRAMES_N = 12
FIREWORK_POS: list[Pos] = [(150, 200), (300, 50), (550, 200)]
FIREWORK_DELAY: list[float] = [0, 500, 1000]


DIGIT_FRAMES: int = 4
DIGIT_SEQUENCE = (0, 1, 2, 3, 2, 1)
DIGIT_FRAME_DUR = 180


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
            self.update_frame(frames, None)
            if self.current_frame in range(FIREWORKS_FRAMES_N):
                self.screen.blit(self.firework_sprites[self.current_frame], self.pos)


class Highscore(Animation):
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__(screen)
        main_path = Path(__file__).resolve().parent / "sprites" / "highscore_32"
        self.digit_sprites: dict[str, list[pg.Surface]] = {str(name): [pg.image.load(
            f"{main_path}/digit_{name}_{frame}.png").convert_alpha()
            for frame in range(DIGIT_FRAMES)]
            for name in range(10)}

        self.center_y = self.digit_sprites["1"][0].get_rect().centery

    def draw_highscore(self, temp_plug: str, dt: float) -> None:
        #print(self.digit_sprites["1"][0].width)
        frames = 0
        while self.animation_elapsed >= DIGIT_FRAME_DUR:
            self.animation_elapsed -= DIGIT_FRAME_DUR
            frames += 1
        self.update_frame(frames, DIGIT_SEQUENCE)
        number = temp_plug.zfill(6)
        for index, digit in enumerate(number):
            self.screen.blit(self.digit_sprites[digit][self.current_frame],
                             (416 + 24 * index, 300 - self.center_y - 5))


class VictoryView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.button_list: list[MenuButton] = self.create_buttons()
        self.victory_surface: pg.Surface = pg.Surface((screen.width, screen.height), pg.SRCALPHA)
        self.fireworks: dict[str, Fireworks] = {
            name: Fireworks(screen, name, delay, pos)
            for name, delay, pos in zip(FIREWORKS_NAMES, FIREWORK_DELAY, FIREWORK_POS)}
        self.highscore = Highscore(screen)

    def draw_victory(self, mouse_pos: tuple[int, int], dt: float) -> None:
        self.victory_surface.fill((0, 0, 0, 170))
        self.screen.blit(self.victory_surface)
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos, False)
        for firework in FIREWORKS_NAMES:
            self.fireworks[firework].draw_firework(dt)
        #print(self.button_list[1].width)
        self.highscore.draw_highscore("777", dt)

    def create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        button = MenuButton((400, 200), "YOU  WON", None, self.fonts.big_button_font,
                            self.fonts.big_button_hover_font)
        button_list.append(button)
        button = MenuButton((292, 300), "YOUR SCORE", None, self.fonts.mid_button_font,
                            self.fonts.mid_button_hover_font)
        button_list.append(button)
        button = MenuButton((400, 400), "PRESS ANY KEY TO PLAY", None, self.fonts.small_button_font,
                            self.fonts.small_button_hover_font)
        button_list.append(button)
        return button_list
