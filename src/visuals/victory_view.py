import pygame as pg
from .buttons import Fonts, Button


class VictoryView:
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.button_list: list[Button] = self.create_buttons()
        self.victory_surface: pg.Surface = pg.Surface((screen.width, screen.height), pg.SRCALPHA)

    def draw_victory(self, mouse_pos: tuple[int, int]) -> None:
        self.victory_surface.fill((0, 0, 0, 170))
        self.screen.blit(self.victory_surface)
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos, False)

    def create_buttons(self) -> list[Button]:
        button_list: list[Button] = []
        button = Button((400, 200), "YOU  WON", None, self.fonts.big_button_font,
                        self.fonts.big_button_hover_font)
        button_list.append(button)
        button = Button((400, 300), "YOUR SCORE", None, self.fonts.mid_button_font,
                        self.fonts.mid_button_hover_font)
        button_list.append(button)
        button = Button((400, 400), "PRESS ANY KEY TO PLAY", None, self.fonts.small_button_font,
                        self.fonts.small_button_hover_font)
        button_list.append(button)
        return button_list
