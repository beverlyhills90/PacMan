import pygame as pg

from src.core.sound import Sounds
from src.shared_types import GameState, VisualState

from .buttons import Fonts, MenuButton


class MenuView:
    """Main menu: Start Game, Highscore, Instructions and Exit."""

    def __init__(
        self, screen: pg.Surface, fonts: Fonts, sounds: Sounds
    ) -> None:
        self.screen = screen
        self.fonts = fonts
        self.sounds: Sounds = sounds

        self.button_list: list[MenuButton] = self.create_buttons()
        self.pause_menu_buttons: list[MenuButton] = self.create_buttons(True)

    def draw_menu(self, mouse_pos: tuple[int, int], snapshot: GameState) -> None:
        """Draw the menu buttons."""
        if snapshot.status == "pause":
            for button in self.pause_menu_buttons:
                button.draw_button(self.screen, mouse_pos)
        else:
            for button in self.button_list:
                button.draw_button(self.screen, mouse_pos)

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        """Handle a click on the menu.

        Args:
            mouse_pos: Position of the click.

        Returns:
            The screen to switch to, or None if no button was clicked.
        """
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                self.sounds.play_sound("button")
                return button.action
        return None

    def create_buttons(self, pause: bool = False) -> list[MenuButton]:
        """Create the menu buttons."""
        button_list: list[MenuButton] = []
        if pause is False:
            start_buton = MenuButton(
                (400, 200),
                "Start Game",
                "start",
                self.fonts.mid_button_font,
                self.fonts.mid_button_hover_font,
            )
            button_list.append(start_buton)
        else:
            resume_buton = MenuButton(
                (400, 200),
                "Resume Game",
                "start",
                self.fonts.mid_button_font,
                self.fonts.mid_button_hover_font,
            )
            button_list.append(resume_buton)

        highscore_button = MenuButton(
            (400, 300),
            "Highscore",
            "highscore",
            self.fonts.mid_button_font,
            self.fonts.mid_button_hover_font,
        )
        button_list.append(highscore_button)

        controls_button = MenuButton(
            (400, 400),
            "Instructions",
            "controls",
            self.fonts.mid_button_font,
            self.fonts.mid_button_hover_font,
        )
        button_list.append(controls_button)

        exit_button = MenuButton(
            (400, 500),
            "Exit",
            "exit",
            self.fonts.mid_button_font,
            self.fonts.mid_button_hover_font,
        )
        button_list.append(exit_button)

        return button_list
