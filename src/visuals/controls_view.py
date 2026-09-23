import pygame as pg
from .buttons import MenuButton, Fonts
from src.core.sound import Sounds


CONTROL_LIST: list[str] = ["God Mode - G", "Skip Level - L",
                           "Plus Live - 1", "Slow Ghosts - 0",
                           "Infinite Time - T"]


class ControlsView():
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts = fonts
        self.sounds: Sounds = Sounds()

        self.buttons: list[MenuButton] = self._create_buttons()
        self.controls: list[MenuButton] = self._create_controls()

    def draw_control_menu(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.buttons:
            button.draw_button(self.screen, mouse_pos)
        for control in self.controls:
            control.draw_button(self.screen, mouse_pos, False)

    def handle_input(self, mouse_pos: tuple[int, int]):
        for button in self.buttons:
            if button.button_rect.collidepoint(mouse_pos) is True:
                self.sounds.play_sound("eat_pac_gum")
                return button.action
        return None

    def _create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        back_button = MenuButton((50, 30), "Back", "menu",
                                 self.fonts.small_button_font, self.fonts.small_button_hover_font)
        button_list.append(back_button)
        return button_list

    def _create_controls(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        i = 0
        for control in CONTROL_LIST:
            control_button = MenuButton((400, 200 + i * 50), control, None,
                                        self.fonts.mid_button_font,
                                        self.fonts.mid_button_hover_font)
            button_list.append(control_button)
            i += 1

        return button_list
