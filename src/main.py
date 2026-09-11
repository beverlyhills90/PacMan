from argparse import ArgumentParser, Namespace
from pathlib import Path
from parcing import ParsingError, validation
from sys import stderr


def main() -> None:
    args = argument_parser()
    config_path = args.config
    try:
        validation(config_path)
    except ParsingError as e:
        print(e, file=stderr)


def argument_parser() -> Namespace:
    parser = ArgumentParser("pacman")
    parser.add_argument("--config", help="path to config file",
                        default=Path("config.json"), type=Path)
    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
