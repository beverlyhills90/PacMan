import pygame as pg
from .buttons import Button, Fonts
from shared_types import GameState


class HudView():
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts

    def draw_hud(self, snapshot: GameState, mouse_pos: tuple[int, int]) -> None:
        button_list = self.create_buttons(snapshot)
        for button in button_list:
            button.draw_button(self.screen, mouse_pos, False)

    def create_buttons(self, snapshot: GameState) -> list[Button]:
        button_list: list[Button
        ] = []
        button_names = [f"Score:{snapshot.score}",
                        f"Lives:{snapshot.lives}", f"Level:{snapshot.level}"]
        button_centers = [(100, 750), (250, 750), (400, 750)]
        for name, center in zip(button_names, button_centers):
            button = Button(center, name, None, self.fonts.small_button_font,
                            self.fonts.small_button_hover_font)
            button_list.append(button)
        return button_list
