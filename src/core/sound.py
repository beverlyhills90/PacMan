from pathlib import Path
from typing import Literal

from just_playback import Playback

Sound = Literal["eat_pac_gum", "eat_ghost", "game_lost", "victory"]


class Sounds:
    def __init__(self) -> None:
        self.chomp_toggle: bool = False
        sound_path_01 = str(
            Path(__file__).resolve().parent
            / "sounds"
            / "03-pac-man-eating-the-pac-dot.mp3"
        )
        sound_path_02 = str(
            Path(__file__).resolve().parent
            / "sounds"
            / "03-pac-man-eating-the-pac-dot.mp3"
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
        try:
            self.eat_pac_gum01 = Playback(path_to_file=sound_path_01)
            self.eat_pac_gum02 = Playback(path_to_file=sound_path_02)
            self.eat_ghost = Playback(path_to_file=sound_path_03)
            self.fail = Playback(path_to_file=sound_path_04)
            self.win = Playback(path_to_file=sound_path_05)
        except Exception:
            pass

    def play_sound(self, sound: Sound) -> None:
        if sound == "eat_pac_gum":
            if not self.chomp_toggle:
                self.eat_pac_gum02.play()
                self.chomp_toggle = not self.chomp_toggle
            else:
                self.eat_pac_gum01.play()
                self.chomp_toggle = not self.chomp_toggle
        if sound == "eat_ghost":
            self.eat_ghost.play()
        if sound == "game_lost":
            self.fail.play()
        if sound == "victory":
            self.win.play()
