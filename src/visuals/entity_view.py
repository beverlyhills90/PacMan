import pygame as pg
from shared_types import Grid, PacmanView, GameState, Direction
from .game_layout import GameLayout
from game import Game
from abc import ABC

DIRECTIONS: tuple[Direction, ...] = ("right", "down", "left", "up")
PACMAN_SPRITES_N = 4


class Entity(ABC):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.game_layout: GameLayout = game_layout
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, frames: int) -> None:
        self.current_frame = (self.current_frame + frames) % PACMAN_SPRITES_N

    def update_time(self, dt: float) -> None:
        self.animation_elapsed = self.animation_elapsed + dt * 1000


class Pacman(Entity):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        super().__init__(screen, game_layout)
        self.pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [pg.transform.scale(pg.image.load(
                f"visuals/sprites/pacman/pacman_{direction}_{frame}.png").convert_alpha(),
                (35, 35))
                for frame in range(PACMAN_SPRITES_N)]
            for direction in DIRECTIONS
        }

    def draw_pacman(self, pacman_state: PacmanView, dt: float) -> None:
        self.update_time(dt)
        x, y = self.game_layout.tiles_to_coordinates(pacman_state.pos)
        direction = pacman_state.facing
        moving = pacman_state.moving
        frames = 0
        if moving:
            while self.animation_elapsed >= 100:
                self.animation_elapsed -= self.animation_elapsed
                frames += 1
        self.update_frame(frames)
        sprite = self.pacman_sprites[direction][self.current_frame]
        # hitbox_surface = pg.Surface(sprite.size, pg.SRCALPHA)
        # hitbox = pg.draw.rect(hitbox_surface, (0, 50, 0, 120),
        #                      sprite.get_rect(), border_radius=5)
        self.screen.blit(sprite, (x, y))


class Ghost(Entity):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout) -> None:
        super().__init__(screen, game_layout)


class EntityView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen
        self.pacman: Pacman = Pacman(screen, game_layout)
        self.ghosts: list[Ghost] = self.create_ghosts()

    def draw_entities(self, game: Game, dt: float) -> None:
        snapshot = game.snapshot()

        self.pacman.draw_pacman(snapshot.player, dt)

    def create_ghosts(self) -> list[Ghost]:
        pass
