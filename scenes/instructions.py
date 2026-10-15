import pygame
from scenes.base import Scene


class Instructions(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.width, self.height = self.app.window.get_size()

        try:

            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (self.width, self.height)
            )

            self.scroll_panel = pygame.image.load(
                "assets/scroll_panel.png").convert_alpha()
            self.scroll_panel = pygame.transform.smoothscale(
                self.scroll_panel, (400, 550)
            )

            self.panel_w, self.panel_h = self.scroll_panel.get_size()

            self.font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 40)

        except (pygame.error, FileNotFoundError):
            print("Error: could not load menu assets")
            self.app.running = False

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        panel_x = self.width // 2 - self.panel_w // 2
        panel_y = self.height // 6

        screen.blit(self.scroll_panel, (panel_x, panel_y))
