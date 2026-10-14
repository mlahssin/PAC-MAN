import pygame
from scenes.menu import MenuScene
from scenes.game_over import GameOver
from scenes.instructions import Instructions


class App:

    def __init__(self):

        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.scenes = {
            "menu": MenuScene(self),
            "game_over": GameOver(self),
            "instructions": Instructions(self),
        }
        self.current_scene = self.scenes["menu"]
        self.running = True
        self.fps = 60

    def change_scene(self, scene):
        print("!!!! CHANGE SCENE!!!!!!!")
        print("scene:", scene)
        self.current_scene = scene
        self.scenes[scene]

    def run(self):

        menu = MenuScene(self)

        menu_sur = pygame.Surface((200, 200), pygame.SRCALPHA)

        pygame.display.set_caption("PAC MAN")

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                menu.handle_event(event)
                menu.draw(menu_sur)

            self.window.fill((150, 150, 123))
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()


app = App()

app.run()
