import sys
import json
from typing import Any
from pydantic import BaseModel, Field, ValidationError


class Level(BaseModel):
    """Size of one level.

    Attributes:
        width: Number of maze columns (5..30). Defaults to 15.
        height: Number of maze rows (5..30). Defaults to 15.
    """

    width: int = Field(default=15, ge=5, le=30, strict=True)
    height: int = Field(default=15, ge=5, le=30, strict=True)


class Settings(BaseModel):
    """All game settings validated from the config file.

    Attributes:
        highscore_filename: File path for persisting the high-score list.
        lives: Number of starting lives (1..3). Defaults to 3.
        pacgum: Total number of pacgums per level. Defaults to 42.
        points_per_pacgum: Score per collected pacgum. Defaults to 10.
        points_per_super_pacgum: Score per super-pacgum. Defaults to 50.
        points_per_ghost: Score per eaten ghost. Defaults to 200.
        seed: Random seed for the first level. Defaults to 42.
        level_max_time: Time limit per level in seconds. Defaults to 90.
        levels: List of Level objects (at least one). Defaults to 10 levels.
    """

    highscore_filename: str = Field(default="highscores.json")
    lives: int = Field(default=3, ge=1, le=3, strict=True)
    pacgum: int = Field(default=42, ge=0, le=500, strict=True)
    points_per_pacgum: int = Field(default=10, ge=0, strict=True)
    points_per_super_pacgum: int = Field(default=50, ge=0, strict=True)
    points_per_ghost: int = Field(default=200, ge=0, strict=True)
    seed: int = Field(default=42, ge=0, strict=True)
    level_max_time: int = Field(default=90, ge=10, le=600, strict=True)
    levels: list[Level] = Field(default=[Level()] * 10, min_length=1)


class Config:
    """Load, strip comments from, and validate a JSON config file.

    Attributes:
        file: Path to the JSON config file.
        values: Raw parsed key-value pairs from the file.
    """

    def __init__(self, file: str) -> None:
        """Store the file path for later loading.

        Args:
            file: Path to the JSON config file.
        """
        self.file = file
        self.values: dict[str, Any] = {}

    def load_to_dict(self, text: str) -> dict[str, Any]:
        """Parse a JSON string into a dict, falling back to empty on error.

        Args:
            text: JSON text with comments already removed.

        Returns:
            A dict of parsed values, or an empty dict on parse failure.
        """
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

    def load(self) -> Settings:
        """Read the file, strip comments, parse, and validate.

        Returns:
            A validated Settings instance (with defaults for bad values).
        """
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
        """Validate a raw dict against Settings, warning on bad keys/values.

        Args:
            data: Dict of raw config values to validate.

        Returns:
            A Settings instance with defaults substituted for invalid values.
        """
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
            try:
                return Settings(**data)
            except ValidationError:
                self.warn("too many invalid values, using all defaults")
                return Settings()

    def remove_comments(self) -> str:
        """Read the file and strip lines that start with '#'.

        Returns:
            The file contents as a string with comment lines removed,
            or an empty string if the file cannot be opened.
        """
        lines = []

        try:
            with open(self.file) as file:
                for line in file:
                    if not line.strip().startswith("#"):
                        lines.append(line)

        except OSError as error:
            self.warn(f"cannot open '{self.file}': {error.strerror}, "
                      "using defaults")
            return ""

        except UnicodeDecodeError:
            self.warn(f"'{self.file}' is not a text file, using defaults")
            return ""

        return "".join(lines)
