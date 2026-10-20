from pathlib import Path
import json

class Leaderboard_Engine:
    def __init__(self):
        self.scores = []
        self.file_name = Path("scores.json")
        self.create_json_file()
        self.load_scores()

    def create_json_file(self):
        if not self.file_name.exists():
            self.file_name.touch()
            with open(self.file_name, "w") as f:
                json.dump(self.scores, f, indent=4)
    
    def load_scores(self):
        # try:
        with open(self.file_name, "r") as f:
            self.scores = json.load(f)
        # except Exception as e:
        #     print("here is where the problem ")
    
    def add_scores(self, name, score):
        self.scores.append({
            "name": name,
            "score": score
        })
        self.sorted_scores()
        self.save_scores()

    def sorted_scores(self):
        self.scores = sorted(
            self.scores,
            key=lambda x: x["score"],
            reverse=True
        )

    def save_scores(self):
        self.scores = self.scores[:10]

        with open(self.file_name, "w") as f:
            json.dump(self.scores, f, indent=4)
