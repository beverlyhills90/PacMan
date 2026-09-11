from pathlib import Path
from pydantic import BaseModel, ValidationError, Field, model_validator
import json
from typing import Any


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Level(BaseModel):
    width: Any = Field(default=20)
    height: Any = Field(default=20)
    seed: Any = Field(default=None)


class Config(BaseModel):
    highscore_filename: Path = Field(default=Path("highscores.json"))
    lives: Any = Field(default=3)
    pacgum: Any = Field(default=42)
    points_per_pacgum: Any = Field(default=10)
    points_per_super_pacgum: Any = Field(default=50)
    points_per_ghost: Any = Field(default=200)
    level_max_time: Any = Field(default=90)
    levels: Any = Field(default_factory=list)

    @model_validator(mode="after")
    def levels_validator(self):
        if type(self.levels) is not list:
            print(f"Config warning: levels: {self.levels} is not list. "
                  "Deleting pshhhh.....")
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
        i = 10 - missing_levels
        while i < 10:
            if i == 0:
                level: Level = Level(seed=42)
            else:
                level: Level = Level()
            self.levels.append(level)
            i += 1

    def check_size(self) -> None:
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
    def config_validator(self):
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

        if type(self.pacgum) is not int:
            print(
                "Config warning: 'pacgum' must be an integer; "
                "using default value 42."
            )
            self.pacgum = 42
        elif self.pacgum < 20 or self.pacgum > 80:
            print(
                f"Config warning: 'pacgum' must be between 20 and 80; "
                f"got {self.pacgum!r}, using default value 42."
            )
            self.pacgum = 42

        if type(self.points_per_super_pacgum) is not int:
            print(
                "Config warning: 'points_per_super_pacgum' must be an "
                "integer; using default value 50."
            )
            self.points_per_super_pacgum = 50
        elif self.points_per_super_pacgum < 25 or self.points_per_super_pacgum > 100:
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
    try:
        raw_congfig = config_path.read_text("utf-8")
        wipe_coments: list[str] = []
        for line in raw_congfig.splitlines():
            line = line.lstrip()
            if line.startswith("#") is False:
                wipe_coments.append(line)
            else:
                wipe_coments.append("")
        clean_config = "\n".join(wipe_coments)
        json_config = json.loads(clean_config)
        config = Config.model_validate(json_config)
        return config

    except OSError as e:
        target = e.filename if e.filename else ""
        raise ParsingError(f"Error: {e} '{target}'")
    except json.JSONDecodeError as e:
        raise ParsingError(
            f"Json Error: {e.msg} on line {e.lineno - 1}, column {e.colno}")
