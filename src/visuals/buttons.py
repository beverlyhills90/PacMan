from shared_types import VisualState
import pygame as pg


class Button:
    def __init__(self, center: tuple[int, int], text: str, action: VisualState,
                 normal_font: pg.font.Font, hover_font: pg.font.Font) -> None:
        self.text_surface: pg.Surface = normal_font.render(text, False, "white")
        self.button_rect = self.text_surface.get_rect(center=center)
        self.hover_text_surface: pg.Surface = hover_font.render(text, False, "red")
        self.hover_rect = self.hover_text_surface.get_rect(center=center)
        self.action: VisualState = action

    def draw_button(self, screen: pg.Surface, mouse_pos: tuple[int, int]) -> None:
        hovered = self.button_rect.collidepoint(mouse_pos)
        if hovered is False:
            screen.blit(self.text_surface, self.button_rect)
        else:
            screen.blit(self.hover_text_surface, self.hover_rect)
