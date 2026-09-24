from json import JSONDecodeError
from pathlib import Path

import pygame as pg

from src.core.sound import Sounds
from src.highscore import TopTen
from src.shared_types import VisualState

from .abs_classes import Highscore, get_centered_x
from .buttons import Fonts, MenuButton


class HighscoreView:
    """Highscore screen: the top 10, or the error if the file is unreadable."""
    def __init__(
        self, screen: pg.Surface, fonts: Fonts, highscore_path: Path
    ) -> None:
        self.screen: pg.Surface = screen
        self.fonts: Fonts = fonts
        self.sound: Sounds = Sounds()

        self.highscore_list: list[tuple[str, int]] | str = self._get_top_ten(
            highscore_path
        )
        if isinstance(self.highscore_list, str):
            self.error: list[MenuButton] = self._get_error_msg(
                self.highscore_list
            )
        self.highscore = Highscore(screen)
        self.button_list: list[MenuButton] = self._create_buttons()

    def draw_highscore_menu(
        self, mouse_pos: tuple[int, int], dt: float
    ) -> None:
        """Draw the highscore table (or the error) and the Back button."""
        for button in self.button_list:
            button.draw_button(self.screen, mouse_pos)
        if isinstance(self.highscore_list, str):
            for message in self.error:
                message.draw_button(self.screen, mouse_pos, False)
        else:
            self.draw_highscore(self.highscore_list, dt)

    def handle_input(self, mouse_pos: tuple[int, int]) -> VisualState | None:
        """Handle a click on the screen.

        Args:
            mouse_pos: Position of the click.

        Returns:
            The screen to switch to, or None if no button was clicked.
        """
        for button in self.button_list:
            if button.button_rect.collidepoint(mouse_pos) is True:
                self.sound.play_sound("button")
                return button.action
        return None

    def _create_buttons(self) -> list[MenuButton]:
        button_list: list[MenuButton] = []

        back_button = MenuButton(
            (50, 30),
            "Back",
            "menu",
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(back_button)

        return button_list

    def draw_highscore(
        self, highscore: list[tuple[str, int]], dt: float
    ) -> None:
        """Draw one row per entry: the name followed by its score.

        Args:
            highscore: (name, score) pairs, best first.
            dt: Seconds elapsed since the previous frame.
        """
        y = 102
        for name, score in highscore:
            name_surface = self.fonts.mid_button_font.render(
                name, False, "white"
            )
            x = get_centered_x(name_surface.width, self.screen.width)
            name_rect = name_surface.get_rect(bottomleft=(x, y))
            self.screen.blit(name_surface, name_rect)
            self.highscore.draw_highscore(score, dt, x + name_surface.width, y)
            y += 70

    def _get_error_msg(self, message: str) -> list[MenuButton]:
        button_list: list[MenuButton] = []
        message_list = message.split()
        prev_string: list[str] = []
        button_fitting: list[str] = []
        i = 0
        for word in message_list:
            # print(word)
            button_fitting.append(word)
            str_surface = self.fonts.small_button_font.render(
                "".join(button_fitting), False, "white"
            )
            if str_surface.width > 300:
                button = MenuButton(
                    (400, 200 + 50 * i),
                    " ".join(prev_string),
                    None,
                    self.fonts.small_button_font,
                    self.fonts.small_button_hover_font,
                )
                button_list.append(button)
                prev_string.clear()
                prev_string.append(button_fitting[-1])
                button_fitting.clear()
                button_fitting.append(prev_string[-1])
                i += 1
            else:
                prev_string.append(word)
        button = MenuButton(
            (400, 200 + 50 * i),
            " ".join(prev_string),
            None,
            self.fonts.small_button_font,
            self.fonts.small_button_hover_font,
        )
        button_list.append(button)

        return button_list

    def _get_top_ten(self, file_path: Path) -> list[tuple[str, int]] | str:
        try:
            top_ten = TopTen.read_top_ten(file_path)
            highscore_list: list[tuple[str, int]] = [
                (player.nickname, player.score) for player in top_ten.players
            ]
            return highscore_list[:10]
        except (OSError, JSONDecodeError) as e:
            print(e)
            return str(e)
