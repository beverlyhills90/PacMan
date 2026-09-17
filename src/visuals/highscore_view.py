import pygame as pg
from .buttons import Button, Fonts
from shared_types import VisualState


class HighscoreView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts

        self.button_list: list[Button] = self._create_buttons()

    def draw_highscore(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos)

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                return button.action
        return None

    def _create_buttons(self) -> list[Button]:
        button_list: list[Button] = []

        back_button = Button((50, 30), "Back", "menu",
                             self.fonts.small_button_font, self.fonts.small_button_hover_font)
        button_list.append(back_button)

        return button_list
