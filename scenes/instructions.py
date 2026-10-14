import pygame
from scenes.base import Scene


class Instructions(Scene):

    def __init__(self, app):
        super().__init__(app)
        print("Inside: instructions")

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_1:
            print("game")
            self.app.change_scene("game")

        if event.key == pygame.K_2:
            print("game_over")
            self.app.change_scene("game_over")

        if event.key == pygame.K_3:
            print("instructions")
            self.app.change_scene("instructions")

        if event.key == pygame.K_q:
            self.app.change_scene("instructions")
