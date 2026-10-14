import pygame
from scenes.menu import MenuScene
from scenes.game_over import GameOver
from scenes.instructions import Instructions


class App:

    def __init__(self):

        self.window = None
        self.clock = None
        self.scenes = {
            "menu": MenuScene(self),
            "game_over": GameOver(self),
            "instructions": Instructions(self),
        }
        self.current_scene = MenuScene
        self.running = True

    def change_scene(self, scene):
        print("!!!! CHANGE SCENE!!!!!!!")
        print("scene:", scene)
        self.current_scene = scene
        self.scenes[scene]

    def run():
        
pygame.init()

app = App()

menu = MenuScene(app)

screen = pygame.display.set_mode((500, 500))

# menu.handle_event(event)

pygame.display.set_caption("MENU")

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        menu.handle_event(event)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
