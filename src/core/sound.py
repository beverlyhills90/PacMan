from pathlib import Path
from typing import Literal

from just_playback import Playback

Sound = Literal["eat_pac_gum", "eat_ghost", "game_lost"]


class Sounds:
    def __init__(self) -> None:
        self.firssecondeat: bool = False
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
        try:
            self.eat_pac_gum01 = Playback(path_to_file=sound_path_01)
            self.eat_pac_gum02 = Playback(path_to_file=sound_path_02)
            self.eat_ghost = Playback(path_to_file=sound_path_03)
            self.fail = Playback(path_to_file=sound_path_04)
        except Exception:
            pass

    def play_sound(self, sound: Sound) -> None:
        if sound == "eat_pac_gum":
            if not self.firssecondeat:
                self.eat_pac_gum02.play()
                self.firssecondeat = not self.firssecondeat
            else:
                self.eat_pac_gum01.play()
                self.firssecondeat = not self.firssecondeat
        if sound == "eat_ghost":
            self.eat_ghost.play()
        if sound == "game_lost":
            self.fail.play()
