import pygame as pg

from src.shared_types import VisualState

from .abs_classes import Highscore, get_centered_x
from .buttons import Fonts, MenuButton


class HighscoreView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.highscore = Highscore(screen)
        self.button_list: list[MenuButton] = self._create_buttons()

    def draw_highscore_menu(
        self, mouse_pos: tuple[int, int], dt: float
    ) -> None:
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos)
        self.draw_highscore(
            [("Yaroo", 300), ("lolkek", 1500), ("test", 1000000)], dt
        )

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                return button.action
        return None

    def _create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []

        back_button = MenuButton(
            (50, 30),
            "Back",
            "menu",
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(back_button)

        return button_list

    def draw_highscore(
        self, highscore: list[tuple[str, int]], dt: float
    ) -> None:
        y = 100
        for name, score in highscore:
            name_surface = self.fonts.mid_button_font.render(
                name, False, "white"
            )
            x = get_centered_x(name_surface.width, self.screen.width)
            name_rect = name_surface.get_rect(bottomleft=(x, y))
            self.screen.blit(name_surface, name_rect)
            self.highscore.draw_highscore(score, dt, x + name_surface.width, y)
            y += 70
