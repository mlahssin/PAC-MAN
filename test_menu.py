import pygame
from scenes.base import Scene
from scenes.menu import MenuScene
from app import App

pygame.init()

app = App()

menu = MenuScene(app)

screen = pygame.display.set_mode((500, 500))

# menu.handle_event(event)
#flflf
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
