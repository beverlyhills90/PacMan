import pygame as pg

from src.shared_types import VisualState

from .buttons import Fonts, MenuButton


class InputName:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.input_button: MenuButton = MenuButton(
            (400, 200),
            "Enter Your Name:",
            None,
            self.fonts.big_button_font,
            self.fonts.big_button_hover_font,
        )
        self.name: list[str] = []

    def draw_imput_screen(self, mouse_pos: tuple[float, float]) -> None:
        self.input_button.draw_button(self.screen, mouse_pos, False)
        name_surface = MenuButton(
            (400, 250),
            "".join(self.name),
            None,
            self.fonts.mid_button_font,
            self.fonts.mid_button_hover_font,
        )
        name_surface.draw_button(self.screen, mouse_pos, False)

    def handle_input(self, event: pg.Event) -> VisualState | None:
        if event.key == pg.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.key == pg.K_RETURN and len(self.name) >= 3:
            return "menu"
        elif str.isalnum(event.unicode) and len(self.name) <= 10:
            self.name.append(event.unicode)
        return None
