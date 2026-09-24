from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr

import pygame as pg

from src.core.maze_adapter import build_grid_for_level
from src.core.player import Player
from src.core.world import find_start
from src.parsing import ParsingError, validation
from src.visuals.visualiser import Visualiser


def main() -> None:
    """Load the configuration and run the game.

    Configuration, file and pygame errors are printed on stderr
    instead of raising.
    """
    args = argument_parser()
    config_path = args.config

    try:
        pg.init()

        config = validation(config_path)
        grid = build_grid_for_level(config.levels[0])
        player = Player(find_start(grid), 4)
        visualiser = Visualiser(player, config)
        visualiser.main_loop()
    except ParsingError as e:
        print(e, file=stderr)
    except FileNotFoundError as e:
        print(e, file=stderr)
    except pg.error as e:
        print(e, file=stderr)


def argument_parser() -> Namespace:
    """Parse the command line: exactly one path to a config file.

    Returns:
        Parsed arguments, with the path in `config`.
    """
    parser = ArgumentParser("pacman")
    parser.add_argument(
        "config",
        help="path to config file",
        type=Path,
    )
    # default=Path(__file__).resolve().parent.parent / "config.json",

    args: Namespace = parser.parse_args()
    return args
