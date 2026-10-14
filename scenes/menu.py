import pygame
from scenes.base import Scene


class MenuScene(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.options = [
            ("PLAY", "game"),
            ("INSTRUCTIONS", "instructions"),
            ("LEADERBOARD", "leaderboard"),
            ("QUIT", "quit"),
        ]

        self.background = self.load_image("assets/menu_background.jpeg", 300,)
        self.button_img = None

        print("MENU   (1: game, 2: game_over, 3: leaderboard, Q: quit)")

    def load_image(self, path, size):

        try:
            image = pygame.image.load(path)
            image = image.convert_alpha()

        except (pygame.error, FileNotFoundError, OSError):
            return None

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

    def draw(self, screen):

        if self.background is not None:
            screen.blit(self.background, (0, 0))
