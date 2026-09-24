from pathlib import Path
from typing import Literal

from just_playback import Playback

Sound = Literal["eat_pac_gum", "eat_ghost", "game_lost", "victory", "button"]


class Sounds:
    """Loads the game sound effects and plays them by name."""

    def __init__(self) -> None:
        self.chomp_toggle: bool = True
        sound_path_01 = str(
            Path(__file__).resolve().parent
            / "sounds"
            / "03-pac-man-eating-the-pac-dot.mp3"
        )
        sound_path_02 = str(
            Path(__file__).resolve().parent
            / "sounds"
            / "03-pac-man-eating-the-pac-dots02.mp3"
        )
        sound_path_03 = str(
            Path(__file__).resolve().parent / "sounds" / "Eating_The_Ghost.mp3"
        )
        sound_path_04 = str(
            Path(__file__).resolve().parent / "sounds" / "fail_2.mp3"
        )
        sound_path_05 = str(
            Path(__file__).resolve().parent / "sounds" / "win.mp3"
        )
        sound_path_06 = str(
            Path(__file__).resolve().parent / "sounds" / "button.mp3"
        )
        try:
            self.eat_pac_gum01 = Playback(path_to_file=sound_path_01)
        except Exception:
            self.eat_pac_gum01 = None

        try:
            self.eat_pac_gum02 = Playback(path_to_file=sound_path_02)
        except Exception:
            self.eat_pac_gum02 = None

        try:
            self.eat_ghost = Playback(path_to_file=sound_path_03)
        except Exception:
            self.eat_ghost = None
        try:
            self.fail = Playback(path_to_file=sound_path_04)
        except Exception:
            self.fail = None

        try:
            self.win = Playback(path_to_file=sound_path_05)
        except Exception:
            self.win = None

        try:
            self.button = Playback(path_to_file=sound_path_06)
        except Exception:
            self.button = None

    def play_sound(self, sound: Sound) -> None:
        """Play a sound effect.

        Consecutive "eat_pac_gum" calls alternate between two chomp
        sounds.

        Args:
            sound: Name of the effect to play.
        """
        if sound == "eat_pac_gum":
            if not self.chomp_toggle:
                if self.eat_pac_gum02 is not None:
                    self.eat_pac_gum02.play()
                self.chomp_toggle = not self.chomp_toggle
            else:
                if self.eat_pac_gum01 is not None:
                    self.eat_pac_gum01.play()
                self.chomp_toggle = not self.chomp_toggle
        if sound == "eat_ghost":
            if self.eat_ghost is not None:
                self.eat_ghost.play()
        if sound == "game_lost":
            if self.fail is not None:
                self.fail.play()
        if sound == "victory":
            if self.win is not None:
                self.win.play()
        if sound == "button":
            if self.button is not None:
                self.button.play()
