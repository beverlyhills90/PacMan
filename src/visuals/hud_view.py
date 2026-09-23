import pygame as pg

from src.shared_types import GameState

from .buttons import Fonts, HudButton
from .game_layout import GameLayout


class HudView:
    def __init__(
        self, screen: pg.Surface, fonts: Fonts, game_layout: GameLayout
    ) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.game_layout = game_layout
        self.x, self.y = game_layout.get_hud_coordinates()
        self.offset = 170

    def draw_hud(self, snapshot: GameState, mouse_pos: tuple[int, int]) -> None:
        button_list = self.create_buttons(snapshot)
        for button in button_list:
            button.draw_button(self.screen)

    def create_buttons(self, snapshot: GameState) -> list[HudButton]:
        button_list: list[HudButton] = []
        button_names = [f"Score:{snapshot.score}",
                        f"Lives:{snapshot.lives}", f"Level:{snapshot.level}", "Time:"]
        button_centers = [(self.x + self.offset * i, self.y) for i in range(4)]
        for name, center in zip(button_names, button_centers):
            button = HudButton(center, name, self.fonts.small_button_font)
            button_list.append(button)
        return button_list
