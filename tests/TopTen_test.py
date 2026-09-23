from pathlib import Path

from src.highscore import TopTen


def test_read_from_file() -> None:
    tt = TopTen.read_top_ten(
        Path("/Users/og/myubuntu/42repo/PACMAN/highscore.json")
    )
    print(len(tt.players))
    for x in tt.players:
        print(x)


def test_save_to_file() -> None:
    TopTen.save(
        Path("/Users/og/myubuntu/42repo/PACMAN/highscore.json"), 10000000, "xD"
    )
    tt = TopTen.read_top_ten(
        Path("/Users/og/myubuntu/42repo/PACMAN/highscore.json")
    )
    print(len(tt.players))
    for x in tt.players:
        print(x)
