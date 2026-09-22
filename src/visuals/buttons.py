from shared_types import VisualState
import pygame as pg
from pathlib import Path


class Fonts:
    def __init__(self) -> None:
        main_font_path = Path(__file__).resolve(
        ).parent / "fonts" / "PressStart2P-vaV7.ttf"
        self.mid_button_font = pg.font.Font(main_font_path, 20)
        self.mid_button_hover_font = pg.font.Font(main_font_path, 25)
        self.small_button_font = pg.font.Font(main_font_path, 15)
        self.small_button_hover_font = pg.font.Font(main_font_path, 20)
        self.big_button_font = pg.font.Font(main_font_path, 30)
        self.big_button_hover_font = pg.font.Font(main_font_path, 35)


class MenuButton:
    def __init__(self, center: tuple[float, float], text: str, action: VisualState | None,
                 normal_font: pg.font.Font, hover_font: pg.font.Font) -> None:
        self.text_surface: pg.Surface = normal_font.render(text, False, "white")
        self.button_rect = self.text_surface.get_rect(center=center)
        self.hover_text_surface: pg.Surface = hover_font.render(text, False, "red")
        self.hover_rect = self.hover_text_surface.get_rect(center=center)
        self.action: VisualState | None = action
        self.width = self.text_surface.get_height()

    def draw_button(self, screen: pg.Surface, mouse_pos: tuple[float, float],
                    hovered_state: bool = True) -> None:
        if hovered_state:
            hovered = self.button_rect.collidepoint(mouse_pos)
            if hovered is False:
                screen.blit(self.text_surface, self.button_rect)
            else:
                screen.blit(self.hover_text_surface, self.hover_rect)
        else:
            screen.blit(self.text_surface, self.button_rect)


class HudButton():
    def __init__(self, left: tuple[int, int], text: str, normal_font: pg.font.Font) -> None:
        self.text_surface: pg.Surface = normal_font.render(text, False, "white")
        self.button_rect = self.text_surface.get_rect(topleft=left)

    def draw_button(self, screen: pg.Surface) -> None:
        screen.blit(self.text_surface, self.button_rect)
