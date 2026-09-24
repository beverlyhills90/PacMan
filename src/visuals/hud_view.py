import pygame as pg

from src.shared_types import GameState

from .buttons import Fonts, HudButton
from .game_layout import GameLayout


class HudView:
    """In-game HUD: score, lives, level and time left."""
    def __init__(
        self, screen: pg.Surface, fonts: Fonts, game_layout: GameLayout
    ) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.game_layout = game_layout
        self.x, self.y = game_layout.get_hud_coordinates()
        self.offset = 170

    def draw_hud(self, snapshot: GameState, mouse_pos: tuple[int, int]) -> None:
        """Draw the HUD for the current frame."""
        button_list = self.create_buttons(snapshot)
        for button in button_list:
            button.draw_button(self.screen)

    def create_buttons(self, snapshot: GameState) -> list[HudButton]:
        """Build the HUD labels from the snapshot."""
        button_list: list[HudButton] = []
        button_names = [
            f"Score:{snapshot.score}",
            f"Lives:{snapshot.lives}",
            f"Level:{snapshot.level}",
            f"Time:{snapshot.time_left}",
        ]
        button_centers = [(self.x + self.offset * i, self.y) for i in range(4)]
        for name, center in zip(button_names, button_centers):
            button = HudButton(center, name, self.fonts.small_button_font)
            button_list.append(button)
        return button_list
