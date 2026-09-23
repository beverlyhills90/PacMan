from pathlib import Path

import pygame as pg

from src.shared_types import Direction, GameState, GhostView, Grid, PacmanView

from .abs_classes import Animation
from .errors import VisulisationError
from .game_layout import GameLayout

DIRECTIONS: tuple[Direction, ...] = ("right", "down", "left", "up")
PACMAN_SPRITES_N = 4
PACMAN_SEQUENCE = (0, 1, 2, 3, 2, 1, 0)
PACMAN_FRAME_DUR = 100
GHOSTS_SPRITES_N = 2
GHOST_FRAME_DUR = 80
GHOST_SEQUENCE = (0, 1, 0)


class Pacman(Animation):
    def __init__(
        self, screen: pg.Surface, game_layout: GameLayout, size: int
    ) -> None:
        super().__init__(screen)
        self.game_layout: GameLayout = game_layout
        main_path = Path(__file__).resolve().parent / "sprites" / "pacman"
        self.pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [
                pg.transform.scale(
                    pg.image.load(
                        f"{main_path}/pacman_{direction}_{frame}.png"
                    ).convert_alpha(),
                    (size, size),
                )
                for frame in range(PACMAN_SPRITES_N)
            ]
            for direction in DIRECTIONS
        }
        self.dim_pacman_sprites: dict[str, list[pg.Surface]] = {
            direction: [
                pacman_sprite.copy()
                for pacman_sprite in self.pacman_sprites[direction]
            ]
            for direction in DIRECTIONS
        }

    def draw_pacman(
        self,
        pacman_state: PacmanView,
        dt: float,
        god_mode: bool,
    ) -> None:
        self.update_time(dt)
        x, y = self.game_layout.tiles_to_coordinates(pacman_state.pos)
        direction = pacman_state.facing
        moving = pacman_state.moving
        frames = 0
        if moving:
            while self.animation_elapsed >= PACMAN_FRAME_DUR:
                self.animation_elapsed -= PACMAN_FRAME_DUR
                frames += 1
        self.update_frame(frames, PACMAN_SEQUENCE)
        if god_mode is True:
            sprite = self.dim_pacman_sprites[direction][self.current_frame]
            sprite.set_alpha(120)
        else:
            sprite = self.pacman_sprites[direction][self.current_frame]

        self.screen.blit(sprite, (x, y))


class Ghost(Animation):
    def __init__(
        self, screen: pg.Surface, game_layout: GameLayout, size: int, name: str
    ) -> None:
        super().__init__(screen)
        self.game_layout: GameLayout = game_layout
        main_path = Path(__file__).resolve().parent / "sprites" / "ghosts"
        self.name: str = name
        self.ghost_sprites: dict[str, list[pg.Surface]] = {
            direction: [
                pg.transform.scale(
                    pg.image.load(
                        f"{main_path}/ghost_{name}_{direction}_{frame}.png"
                    ).convert_alpha(),
                    (size, size),
                )
                for frame in range(GHOSTS_SPRITES_N)
            ]
            for direction in DIRECTIONS
        }

    def draw_ghost(self, snapshot: GameState, dt: float) -> None:
        self.update_time(dt)
        ghost = self.find_ghost(snapshot)
        direction = ghost.facing
        x, y = self.game_layout.tiles_to_coordinates(ghost.pos)
        frames = 0
        while self.animation_elapsed >= GHOST_FRAME_DUR:
            frames += 1
            self.animation_elapsed -= GHOST_FRAME_DUR
        self.update_frame(frames, GHOST_SEQUENCE)
        sprite = self.ghost_sprites[direction][self.current_frame]
        self.screen.blit(sprite, (x, y))

    def find_ghost(self, snapshot: GameState) -> GhostView:
        for ghost_view in snapshot.ghosts:
            if ghost_view.name == self.name:
                return ghost_view
        raise VisulisationError(
            "Couldnt find ghost: how could it happen, mystery....."
        )


class EntityView:
    def __init__(
        self, grid: Grid, game_layout: GameLayout, screen: pg.Surface
    ) -> None:
        self.grid: Grid = grid
        self.game_layout: GameLayout = game_layout
        self.screen: pg.Surface = screen
        self.pacman: Pacman = Pacman(
            screen, game_layout, self.game_layout.tile_size
        )
        self.ghosts: list[Ghost] = self.create_ghosts()

    def draw_entities(self, snapshot: GameState, dt: float) -> None:
        self.pacman.draw_pacman(snapshot.player, dt, snapshot.god_mode)
        for ghost in self.ghosts:
            ghost.draw_ghost(snapshot, dt)

    def create_ghosts(self) -> list[Ghost]:
        ghost_list: list[Ghost] = []
        ghost_names: list[str] = ["blinky", "pinky", "inky", "clyde"]
        for name in ghost_names:
            ghost = Ghost(
                self.screen, self.game_layout, self.game_layout.tile_size, name
            )
            ghost_list.append(ghost)
        return ghost_list
