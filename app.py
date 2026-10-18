import pygame
from scenes.game import GameScene
from scenes.menu import MenuScene
from scenes.game_over import GameOver
from scenes.victory import Victory
from scenes.pause import Pause
from scenes.instructions import Instructions
from scenes.leaderboard import Leaderboard


class App:

    def __init__(self, width, height):

        pygame.init()
        pygame.display.set_caption("PAC MAN")

        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.scenes = {
            "game": GameScene(self),
            "menu": MenuScene(self),
            "instructions": Instructions(self),
            "leaderboard": Leaderboard(self),
            "game_over": GameOver(self),
            "victory": Victory(self),
            "pause": Pause(self)
        }
        self.current_scene = self.scenes["instructions"]
        self.running = True
        self.fps = 60

    def change_scene(self, scene):
        self.current_scene = self.scenes[scene]

    def run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_scene.handle_event(event)

            dt = self.clock.tick(self.fps)
            self.current_scene.update(dt)
            self.current_scene.draw(self.window)
            pygame.display.flip()

        pygame.quit()


app = App(2100, 1500)
app.run()
