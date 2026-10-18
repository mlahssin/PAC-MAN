import pygame
from scenes.base import Scene

# the layout was designed for this window size
DESIGN_W = 1200
DESIGN_H = 800


class MenuScene(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.options = ["PLAY", "INSTRUCTIONS", "LEADERBOARD", "QUIT"]
        self.scenes = ["game", "instructions", "leaderboard", "quit"]

        width, height = self.app.window.get_size()

        # how much bigger than the design: 2100x1500 -> 1.75
        self.scale = min(width / DESIGN_W, height / DESIGN_H)
        # empty space left at the top so the layout is centered vertically
        self.top = (height - int(DESIGN_H * self.scale)) // 2

        try:
            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (width, height))

            self.button = pygame.image.load(
                "assets/buttons/menu_button.png").convert_alpha()
            self.button = pygame.transform.smoothscale(
                self.button, (self.s(380), self.s(85)))

            self.font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", self.s(40))

        except (pygame.error, FileNotFoundError):
            print("Error: could not load menu assets")
            self.app.running = False
            return

        # one Rect per button, used to draw AND to detect clicks
        self.button_rects = []
        y = self.y(400)
        for i in range(4):
            rect = self.button.get_rect(midtop=(width // 2, y))
            self.button_rects.append(rect)
            y += self.s(80)

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window."""
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window."""
        return self.top + self.s(value)

    def choose(self, index):
        target = self.scenes[index]
        if target == "quit":
            self.app.running = False
        else:
            print(target)
            self.app.change_scene(target)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(4):
                if self.button_rects[i].collidepoint(event.pos):
                    self.choose(i)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for i in range(4):
            rect = self.button_rects[i]
            screen.blit(self.button, rect)

            text = self.font.render(self.options[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect.move(self.s(12), 0))
