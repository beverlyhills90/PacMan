import pygame as pg
from .buttons import Fonts, MenuButton
from src.core.sound import Sounds
from src.shared_types import VisualState


class PauseView():
    def __init__(self, screen: pg.Surface, fonts: Fonts) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.sound: Sounds = Sounds()
        self.buttons: list[MenuButton] = self._create_buttons()

    def draw_pause(self, mouse_pos: tuple[float, float]) -> None:
        pause_surface = pg.Surface((800, 800), pg.SRCALPHA)
        pause_surface.fill((0, 0, 0, 100))
        self.screen.blit(pause_surface)
        for button in self.buttons:
            button.draw_button(self.screen, mouse_pos)

    def _create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        back_button = MenuButton(
            (400, 350),
            "Back to Menu",
            "menu",
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(back_button)

        game_button = MenuButton(
            (400, 450),
            "Back to Game",
            "playing",
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(game_button)

        return button_list

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        """Handle a click on the screen.

        Args:
            mouse_pos: Position of the click.

        Returns:
            The screen to switch to, or None if no button was clicked.
        """
        for button in self.buttons:
            if button.button_rect.collidepoint(mouse_pos) is True:
                self.sound.play_sound("button")
                return button.action
        return None
