from pathlib import Path
import json
from typing import Any


class Leaderboard_Engine:
    """Persistent high-score engine: reads and writes scores.json.

    Attributes:
        scores: List of dicts with 'name' and 'score' keys, sorted descending.
        file_name: Path to the JSON file used to persist the scores.
    """

    def __init__(self, file_name: str) -> None:
        """Create the score file if needed and load existing scores."""
        self.scores: list[dict[str, Any]] = []
        self.file_name = Path(file_name)
        print("File:", file_name)
        self.create_json_file()
        self.load_scores()

    def create_json_file(self) -> None:
        """Create an empty scores file if it does not already exist."""
        if not self.file_name.exists():
            try:
                self.file_name.touch()
                with open(self.file_name, "w") as f:
                    json.dump(self.scores, f, indent=4)
            except OSError as e:
                print(f"Warning: could not create scores file: {e}")

    def load_scores(self) -> None:
        """Load scores from the JSON file into memory."""
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                # self.scores = [
                #     e for e in data
                #     if isinstance(e, dict)
                #     and "name" in e and "score" in e
                # ]
                self.scores = [
                    e for e in data
                    if isinstance(e, dict)
                    and isinstance(e.get("name"), str)
                    and len(e["name"]) <= 10
                    and all(c.isalnum() or c == " " for c in e["name"])
                    and type(e.get("score")) is int
                    and e["score"] >= 0
                ]
                self.sorted_scores()
                self.scores = self.scores[:10]
            else:
                print("Warning: scores file has unexpected format, resetting.")
                self.scores = []
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"Warning: could not load scores: {e}")
            self.scores = []

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
        try:
            with open(self.file_name, "w") as f:
                json.dump(self.scores, f, indent=4)
        except OSError as e:
            print(f"Warning: could not save scores: {e}")
