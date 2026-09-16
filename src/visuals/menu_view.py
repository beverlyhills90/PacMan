import pygame as pg
from pathlib import Path
from shared_types import VisualState
from .buttons import Button


class MenuView():
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        main_font_path = Path(__file__).resolve(
        ).parent / "fonts" / "PressStart2P-vaV7.ttf"
        self.button_font = pg.font.Font(main_font_path, 20)
        self.button_hover_font = pg.font.Font(main_font_path, 25)
        self.button_list: list[Button] = self.create_buttons()

    def draw_menu(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos)

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                return button.action
        return None

    def create_buttons(self) -> list[Button]:
        button_list: list[Button] = []

        start_buton = Button((400, 200), "Start Game", "start",
                             self.button_font, self.button_hover_font)
        button_list.append(start_buton)

        highscore_button = Button((400, 300), "Highscore", "highscore",
                                  self.button_font, self.button_hover_font)
        button_list.append(highscore_button)

        exit_button = Button((400, 400), "Exit", "exit",
                             self.button_font, self.button_hover_font)
        button_list.append(exit_button)

        return button_list
