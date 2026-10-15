import pygame
from scenes.base import Scene


class MenuScene(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.options = ["PLAY", "INSTRUCTIONS", "LEADERBOARD", "QUIT"]
        self.scenes = ["game", "instructions", "leaderboard", "quit"]

        width, height = self.app.window.get_size()

        try:

            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (width, height)
            )

            self.button = pygame.image.load(
                "assets/buttons/menu_button.png").convert_alpha()
            self.button = pygame.transform.smoothscale(
                self.button, (380, 85)
            )

            self.font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 40)

        except (pygame.error, FileNotFoundError):
            print("Error: could not load menu assets")
            self.app.running = False

        self.button_rects = []
        y = 400
        for i in range(4):
            rect = self.button.get_rect(midtop=(width // 2, y))
            self.button_rects.append(rect)
            y += 80

    def choose(self, index):

        target = self.scenes[index]
        if target == "quit":
            self.app.running = False
        else:
            self.app.change_scene(self.scenes[index])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(4):
                if self.button_rects[i].collidepoint(event.pos):
                    self.choose(i)

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        button_width = self.button.get_width()
        button_height = self.button.get_height()

        x = screen.get_width() // 2
        x -= button_width // 2

        y = 400

        for i in range(4):
            screen.blit(self.button, (x, y))

            text = self.font.render(self.options[i], True, (255, 255, 255))

            center_x = x + button_width // 2
            center_y = y + button_height // 2

            text_x = center_x - text.get_width() // 2
            text_y = center_y - text.get_height() // 2

            screen.blit(text, (text_x + 12, text_y))

            y += 80
