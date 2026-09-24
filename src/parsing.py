import json
from pathlib import Path
from typing import Any, cast

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from src.shared_types import Level


class ParsingError(Exception):
    """Raised when the config file cannot be read or parsed."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Config(BaseModel):
    """Game configuration validated from the JSON config file.

    An invalid or missing value is replaced by its default and a
    warning is printed; unknown keys are ignored.
    """
    highscore_filename: Path = Field(default=Path("highscores.json"))
    lives: Any = Field(default=3)
    difficulty_level: Any = Field(default=2)
    points_per_pacgum: Any = Field(default=10)
    points_per_super_pacgum: Any = Field(default=50)
    points_per_ghost: Any = Field(default=200)
    level_max_time: Any = Field(default=90)
    levels: Any = Field(default_factory=list)

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_filename_validator(cls, value: Any) -> Path:
        """Use the default file name if the value is not a string or a path."""
        if not isinstance(value, (str, Path)):
            print("Highscore filename not valid,set to default\n")
            return Path("highscores.json")
        return Path(value)

    @model_validator(mode="after")
    def levels_validator(self) -> "Config":
        """Make the level list usable.

        Drops invalid entries, pads the list to 10 levels, and fixes
        sizes and seeds.
        """
        if type(self.levels) is not list:
            print(
                f"Config warning: levels: {self.levels} is not list. "
                "Deleting pshhhh....."
            )
            self.levels = []

        self.validate_levels()

        if len(self.levels) < 10:
            missing_levels = 10 - len(self.levels)
            self.create_levels(missing_levels)
            print(
                "Config warning: at least 10 levels are required; "
                f"got {10 - missing_levels}, added {missing_levels} "
                "default level(s)."
            )

        self.check_size()
        self.check_seed()

        return self

    def validate_levels(self) -> None:
        """Keep only the level entries that match the Level model."""
        correct_list: list[Level] = []
        for level in self.levels:
            try:
                correct_level = Level.model_validate(level)
                correct_list.append(correct_level)
            except ValidationError:
                print(
                    "Config warning: invalid level entry was ignored; "
                    f"got {level!r}."
                )
        self.levels = correct_list

    def create_levels(self, missing_levels: int) -> None:
        """Append default levels; the first level of the game gets seed 42.

        Args:
            missing_levels: Number of levels to add.
        """
        i = 10 - missing_levels
        while i < 10:
            level: Level = Level()
            if i == 0:
                level = Level(seed=42)
            self.levels.append(level)
            i += 1

    def check_size(self) -> None:
        """Reset any width or height that is not an integer in 10..50 to 20."""
        for level in self.levels[:]:
            if type(level.height) is not int:
                print(
                    "Config warning: level 'height' must be an integer; "
                    "using default value 20."
                )
                level.height = 20
            elif level.height < 10 or level.height > 50:
                print(
                    "Config warning: level 'height' must be between 10 "
                    f"and 50; got {level.height!r}, using default value 20."
                )
                level.height = 20
            if type(level.width) is not int:
                print(
                    "Config warning: level 'width' must be an integer; "
                    "using default value 20."
                )
                level.width = 20
            elif level.width < 10 or level.width > 50:
                print(
                    "Config warning: level 'width' must be between 10 "
                    f"and 50; got {level.width!r}, using default value 20."
                )
                level.width = 20

    def check_seed(self) -> None:
        """Force seed 42 on the first level and a random seed on the others."""
        if type(self.levels[0].seed) is not int:
            print(
                "Config warning: the first level 'seed' must be an integer; "
                "using fixed value 42."
            )
            self.levels[0].seed = 42
        elif self.levels[0].seed != 42:
            print(
                "Config warning: the first level must use seed 42; "
                f"got {self.levels[0].seed!r}, using 42."
            )
            self.levels[0].seed = 42
        for level in self.levels[1:]:
            if level.seed is not None:
                print(
                    "Config warning: levels after the first must use a "
                    f"random seed; got {level.seed!r}, using null."
                )
                level.seed = None

    @model_validator(mode="after")
    def config_validator(self) -> "Config":
        """Clamp the numeric settings to their allowed ranges.

        Each value that is not an integer or is out of range is replaced
        by its default, with a warning.
        """
        if type(self.lives) is not int:
            print(
                "Config warning: 'lives' must be an integer; "
                "using default value 3."
            )
            self.lives = 3
        elif self.lives < 1 or self.lives > 10:
            print(
                f"Config warning: 'lives' must be between 1 and 10; "
                f"got {self.lives!r}, using default value 3."
            )
            self.lives = 3

        if type(self.difficulty_level) is not int:
            print(
                "Config warning: 'difficulty_level' must be an integer; "
                "using default value 2."
            )
            self.difficulty_level = 2
        elif self.difficulty_level < 1 or self.difficulty_level > 3:
            print(
                f"Config warning: 'difficulty_level' must be between 1 and 3; "
                f"got {self.difficulty_level!r}, using default value 2."
            )
            self.difficulty_level = 2

        if type(self.points_per_super_pacgum) is not int:
            print(
                "Config warning: 'points_per_super_pacgum' must be an "
                "integer; using default value 50."
            )
            self.points_per_super_pacgum = 50
        elif (
            self.points_per_super_pacgum < 25
            or self.points_per_super_pacgum > 100
        ):
            print(
                "Config warning: 'points_per_super_pacgum' must be between "
                f"25 and 100; got {self.points_per_super_pacgum!r}, "
                "using default value 50."
            )
            self.points_per_super_pacgum = 50

        if type(self.points_per_pacgum) is not int:
            print(
                "Config warning: 'points_per_pacgum' must be an integer; "
                "using default value 10."
            )
            self.points_per_pacgum = 10
        elif self.points_per_pacgum < 5 or self.points_per_pacgum > 20:
            print(
                "Config warning: 'points_per_pacgum' must be between 5 "
                f"and 20; "
                f"got {self.points_per_pacgum!r}, using default value 10."
            )
            self.points_per_pacgum = 10

        if type(self.points_per_ghost) is not int:
            print(
                "Config warning: 'points_per_ghost' must be an integer; "
                "using default value 200."
            )
            self.points_per_ghost = 200
        elif self.points_per_ghost < 100 or self.points_per_ghost > 500:
            print(
                "Config warning: 'points_per_ghost' must be between 100 "
                f"and 500; "
                f"got {self.points_per_ghost!r}, using default value 200."
            )
            self.points_per_ghost = 200

        if type(self.level_max_time) is not int:
            print(
                "Config warning: 'level_max_time' must be an integer; "
                "using default value 90."
            )
            self.level_max_time = 90
        elif self.level_max_time < 30 or self.level_max_time > 180:
            print(
                "Config warning: 'level_max_time' must be between 30 and "
                f"180; "
                f"got {self.level_max_time!r}, using default value 90."
            )
            self.level_max_time = 90

        return self


def validation(config_path: Path) -> Config:
    """Read a config file and return the validated configuration.

    Lines whose first non-blank character is "#" are comments and
    are ignored.

    Args:
        config_path: Path to the JSON config file.

    Returns:
        The validated configuration.

    Raises:
        ParsingError: If the file cannot be read, is not UTF-8 or is
            not valid JSON.
    """
    try:
        raw_config = config_path.read_text("utf-8")
        wipe_comments: list[str] = []
        for line in raw_config.splitlines():
            line = line.lstrip()
            if line.startswith("#") is False:
                wipe_comments.append(line)
            else:
                wipe_comments.append("")
        clean_config = "\n".join(wipe_comments)
        json_config = json.loads(clean_config)
        if type(json_config) is not dict:
            print(
                "Config warning: config must be dict "
                f"type, its {type(json_config)}. "
                "Setting everything to default."
            )
            json_config = {}
        config = Config.model_validate(json_config)
        return cast(Config, config)

    except OSError as e:
        target = e.filename if e.filename else ""
        raise ParsingError(f"Error: {e} '{target}'")
    except ValidationError as e:
        raise ParsingError(
            f"Validation Error: {e}"
        )
    except json.JSONDecodeError as e:
        raise ParsingError(
            f"Json Error: {e.msg} on line {e.lineno - 1}, column {e.colno}"
        )
    except UnicodeDecodeError:
        raise ParsingError("Error: config file must be UTF-8 encoded")
