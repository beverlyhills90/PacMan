import pygame as pg
from shared_types import Grid, PacmanView, GhostView, GameState, Direction
from .game_layout import GameLayout
from .errors import VisulisationError
from pathlib import Path
from game import Game
from abc import ABC

DIRECTIONS: tuple[Direction, ...] = ("right", "down", "left", "up")
PACMAN_SPRITES_N = 4
GHOSTS_SPRITES_N = 2


class Entity(ABC):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout,) -> None:
        super().__init__()
        self.screen: pg.Surface = screen
        self.game_layout: GameLayout = game_layout
        self.current_frame: int = 0
        self.animation_elapsed: float = 0

    def update_frame(self, frames: int, sprites_n: int) -> None:
        self.current_frame = (self.current_frame + frames) % sprites_n

    def update_time(self, dt: float) -> None:
        self.animation_elapsed = self.animation_elapsed + dt * 1000


class Pacman(Entity):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout, size: int) -> None:
        super().__init__(screen, game_layout)
        main_path = Path(__file__).resolve().parent / "sprites" / "pacman"
        self.pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [pg.transform.scale(pg.image.load(
                f"{main_path}/pacman_{direction}_{frame}.png").convert_alpha(),
                (size, size))
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
        self.update_frame(frames, PACMAN_SPRITES_N)
        sprite = self.pacman_sprites[direction][self.current_frame]
        # hitbox_surface = pg.Surface(sprite.size, pg.SRCALPHA)
        # hitbox = pg.draw.rect(hitbox_surface, (0, 50, 0, 120),
        #                      sprite.get_rect(), border_radius=5)
        self.screen.blit(sprite, (x, y))


class Ghost(Entity):
    def __init__(self, screen: pg.Surface, game_layout: GameLayout, size: int, name: str) -> None:
        super().__init__(screen, game_layout)
        main_path = Path(__file__).resolve().parent / "sprites" / "ghosts"
        self.name: str = name
        self.ghost_sprites: dict[str, list[pg.Surface]] = {
            direction: [pg.transform.scale(pg.image.load(
                f"{main_path}/ghost_{name}_{direction}_{frame}.png").convert_alpha(),
                (size, size)) for frame in range(GHOSTS_SPRITES_N)] for direction in DIRECTIONS}

    def draw_ghost(self, snapshot: GameState, dt: float) -> None:
        self.update_time(dt)
        ghost = self.find_ghost(snapshot)
        direction = ghost.facing
        x, y = self.game_layout.tiles_to_coordinates(ghost.pos)
        frames = 0
        while self.animation_elapsed >= 80:
            frames += 1
            self.animation_elapsed -= self.animation_elapsed
        self.update_frame(frames, GHOSTS_SPRITES_N)
        sprite = self.ghost_sprites[direction][self.current_frame]
        self.screen.blit(sprite, (x, y))

    def find_ghost(self, snapshot: GameState) -> GhostView:
        for ghost_view in snapshot.ghosts:
            if ghost_view.name == self.name:
                return ghost_view
        raise VisulisationError("Couldnt find ghost: how could it happen, mystery.....")


class EntityView():
    def __init__(self, grid: Grid, game_layout: GameLayout, screen: pg.Surface) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen
        self.pacman: Pacman = Pacman(screen, game_layout, self.game_layout.tile_size)
        self.ghosts: list[Ghost] = self.create_ghosts()

    def draw_entities(self, game: Game, dt: float) -> None:
        snapshot = game.snapshot()

        self.pacman.draw_pacman(snapshot.player, dt)
        for ghost in self.ghosts:
            ghost.draw_ghost(snapshot, dt)

    def create_ghosts(self) -> list[Ghost]:
        ghost_list: list[Ghost] = []
        ghost_names: list[str] = ["blinky", "pinky", "inky", "clyde"]
        for name in ghost_names:
            ghost = Ghost(self.screen, self.game_layout, self.game_layout.tile_size, name)
            ghost_list.append(ghost)
        return ghost_list
