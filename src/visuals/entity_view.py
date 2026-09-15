import pygame as pg
from shared_types import Grid, PacmanView, GameState
from .game_layout import GameLayout
from game import Game


class EntityView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen

        self.pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [pg.transform.scale(pg.image.load(
                f"visuals/sprites/pacman/pacman_{direction}_{frame}.png").convert_alpha(),
                (35, 35))
                for frame in range(4)]
            for direction in ("right", "down", "left", "up")
        }

    def draw_entities(self, game: Game) -> None:
        self.draw_pacman(game)

    def draw_pacman(self, game: Game) -> None:
        game_state: GameState = game.snapshot()
        pacman_state: PacmanView = game_state.player
        x_tile, y_tile = pacman_state.pos
        # print(x_tile, y_tile)
        tile_size = self.game_layout.tile_size
        x = x_tile * tile_size + self.game_layout.get_offset_x()
        y = y_tile * tile_size + self.game_layout.get_offset_y()
        pacman_sprite = self.pacman_sprites["right"][0]
        pacman_hitbox = pg.Surface(pacman_sprite.size, pg.SRCALPHA)
        pg.draw.rect(pacman_hitbox, (0, 50, 0, 120), pacman_sprite.get_rect(), border_radius=5)
        self.screen.blit(pacman_sprite, (x, y))
        self.screen.blit(pacman_hitbox, (x, y))
