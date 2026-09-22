import pygame as pg
from .sprites_storage import SpritesContainer, MenuSprites, MENU_SPRITES_NAMES


class ControlsView():
    def __init__(self, screen: pg.Surface, sprites: SpritesContainer) -> None:
        self.screen: pg.Surface = screen
        self.menu_sprites: MenuSprites = sprites.menu_sprites

    def draw_control_menu(self) -> None:
        for name in MENU_SPRITES_NAMES:
            sprite_center = self.menu_sprites.sprites[name].get_rect(
                center=self.screen.get_rect().center)
            self.screen.blit(self.menu_sprites.sprites[name], sprite_center)
