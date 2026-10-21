import sys
import json
from typing import Any
from pydantic import BaseModel, Field, ValidationError


class Level(BaseModel):
    """Size of one level."""

    width: int = Field(default=15, ge=5, le=30, strict=True)
    height: int = Field(default=15, ge=5, le=30, strict=True)


class Settings(BaseModel):

    highscore_filename: str = Field(default="highscores.json")
    lives: int = Field(default=3, ge=1, le=9, strict=True)
    pacgum: int = Field(default=42, ge=0, le=500, strict=True)
    points_per_pacgum: int = Field(default=10, ge=0, strict=True)
    points_per_super_pacgum: int = Field(default=50, ge=0, strict=True)
    points_per_ghost: int = Field(default=200, ge=0, strict=True)
    seed: int = Field(default=42, ge=0, strict=True)
    level_max_time: int = Field(default=90, ge=10, le=600, strict=True)
    levels: list[Level] = Field(default=[Level()] * 10, min_length=1)


class Config:

    def __init__(self, file):
        self.file = file
        self.values: dict[str, Any] = {}

    def load_to_dict(self, text):

        if not text.strip():
            return {}

        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            self.warn(f"invalid JSON at line {error.lineno} "
                      f"({error.msg}), using defaults")
            return {}

        if not isinstance(data, dict):
            self.warn("the file must contain { ... }, using defaults")
            return {}

        return data

    def load(self):

        text = self.remove_comments()
        data = self.load_to_dict(text)
        return self.validate(data)

    def warn(self, message: str) -> None:
        """Print a clear config message on stderr.

        Args:
            message: The text to show.
        """
        print(f"[config] {message}", file=sys.stderr)

    def validate(self, data: dict[str, Any]) -> Settings:

        for key in data:
            if key not in Settings.model_fields:
                self.warn(f"unknown key '{key}', ignored")

        for key in Settings.model_fields:
            if key not in data:
                self.warn(f"'{key}' is missing, using default")

        try:
            return Settings(**data)
        except ValidationError as error:
            for problem in error.errors():
                key = str(problem["loc"][0])
                self.warn(f"'{key}' is wrong ({problem['msg']}), "
                          "using default")
                data.pop(key, None)
            return Settings(**data)

    def remove_comments(self):

        lines = []

        try:
            with open(self.file) as file:
                for line in file:
                    if not line.strip().startswith("#"):
                        lines.append(line)

        except OSError as error:
            self.warn(f"cannot open '{self.path}': {error.strerror}, "
                      "using defaults")
            return ""

        except UnicodeDecodeError:
            self.warn(f"'{self.file}' is not a text file, using defaults")
            return ""

        return "".join(lines)


config = Config("config.json")
data = config.load()
