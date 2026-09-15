from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr

from core.maze_adapter import build_grid_for_level
from parsing import ParsingError, validation
from visuals.visualiser import Visualiser
from core.player import Player
from game import Game
from core.world import find_start


def main() -> None:
    args = argument_parser()
    config_path = args.config
    visualiser = Visualiser()

    try:
        config = validation(config_path)
        grid = build_grid_for_level(config.levels[0])
        player = Player(find_start(grid), 2)
        game = Game(config, grid, player, [], set(), set(), 3, 90)
        visualiser.set_cur_grid(grid, game, player)
        visualiser.main_loop()
    except ParsingError as e:
        print(e, file=stderr)


def argument_parser() -> Namespace:
    parser = ArgumentParser("pacman")
    parser.add_argument(
        "--config",
        help="path to config file",
        default=Path("/Users/og/myubuntu/42repo/PACMAN/src/config.json"),
        type=Path,
    )
    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
