from scenes.base import Scene


class GameOver(Scene):

    def __init__(self, app):
        super().__init__(app)
        print("CLASS: game over")

    def run(self):
        print("CLASS: game over")
