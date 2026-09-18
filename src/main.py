from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr

from core.maze_adapter import build_grid_for_level
from parsing import ParsingError, validation
from visuals.visualiser import Visualiser
from core.player import Player
from core.world import find_start
import pygame as pg


def main() -> None:
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
    parser = ArgumentParser("pacman")
    parser.add_argument(
        "--config",
        help="path to config file",
        default=Path(__file__).resolve().parent / "config.json",
        type=Path,
    )
    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
