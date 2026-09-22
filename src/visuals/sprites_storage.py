from pathlib import Path
import pygame as pg

MENU_SPRITES_NAMES: list[str] = ["panel", "button_normal", "button_selected", "keycap"]
MENU_SPRITES_SCALING: list[tuple[int, int]] = [(50, 50), (60, 60), (30, 30), (800, 800)]


class MenuSprites:
    def __init__(self) -> None:
        menu_sprites_path: Path = Path(__file__).resolve().parent / "sprites" / "menu_sprites"
        self.sprites: dict[str, pg.Surface] = {name: (pg.image.load(
            f"{menu_sprites_path}/{name}.png").convert_alpha())
            for name in MENU_SPRITES_NAMES}


class SpritesContainer:
    def __init__(self) -> None:
        self.menu_sprites = MenuSprites()
