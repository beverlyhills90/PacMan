import pygame as pg
from shared_types import VisualState
from .buttons import MenuButton, Fonts


class MenuView():
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen = screen
        self.fonts = fonts

        self.button_list: list[MenuButton] = self.create_buttons()

    def draw_menu(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos)

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                return button.action
        return None

    def create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []

        start_buton = MenuButton((400, 200), "Start Game", "start",
                                 self.fonts.mid_button_font, self.fonts.mid_button_hover_font)
        button_list.append(start_buton)

        highscore_button = MenuButton((400, 300), "Highscore", "highscore",
                                      self.fonts.mid_button_font, self.fonts.mid_button_hover_font)
        button_list.append(highscore_button)

        exit_button = MenuButton((400, 400), "Exit", "exit",
                                 self.fonts.mid_button_font, self.fonts.mid_button_hover_font)
        button_list.append(exit_button)

        return button_list
