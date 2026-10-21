from pathlib import Path
import json
from typing import Any


class Leaderboard_Engine:
    """Persistent high-score engine: reads and writes scores.json.

    Attributes:
        scores: List of dicts with 'name' and 'score' keys, sorted descending.
        file_name: Path to the JSON file used to persist the scores.
    """

    def __init__(self) -> None:
        """Create the score file if needed and load existing scores."""
        self.scores: list[dict[str, Any]] = []
        self.file_name = Path("scores.json")
        self.create_json_file()
        self.load_scores()

    def create_json_file(self) -> None:
        """Create an empty scores file if it does not already exist."""
        if not self.file_name.exists():
            self.file_name.touch()
            with open(self.file_name, "w") as f:
                json.dump(self.scores, f, indent=4)

    def load_scores(self) -> None:
        """Load scores from the JSON file into memory."""
        with open(self.file_name, "r") as f:
            self.scores = json.load(f)

    def add_scores(self, name: str, score: int) -> None:
        """Append a new score, sort, and persist the top 10.

        Args:
            name: Player name (max 10 alphanumeric characters).
            score: Non-negative integer score to record.
        """
        self.scores.append({
            "name": name,
            "score": score
        })
        self.sorted_scores()
        self.save_scores()

    def sorted_scores(self) -> None:
        """Sort the score list in descending order in place."""
        self.scores = sorted(
            self.scores,
            key=lambda x: x["score"],
            reverse=True
        )

    def save_scores(self) -> None:
        """Trim to the top 10 and write the scores back to disk."""
        self.scores = self.scores[:10]

        with open(self.file_name, "w") as f:
            json.dump(self.scores, f, indent=4)
