import pygame
from scenes.base import Scene
import time

FONT = "assets/fonts/Bangers-Regular.ttf"
# the layout was designed for this window size
DESIGN_W = 1200
DESIGN_H = 800


class Pause(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.options = ["RESUME", "MAIN MENU"]

        self.width, self.height = self.app.window.get_size()

        # how much bigger than the design: 2100x1500 -> 1.75
        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)
        # empty space left at the top so the layout is centered vertically
        self.top = (self.height - int(DESIGN_H * self.scale)) // 2

        try:
            self.shade = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.shade.fill((0, 5, 0, 200))

            self.button = pygame.image.load(
                "assets/buttons/menu_button.png").convert_alpha()
            self.button = pygame.transform.smoothscale(
                self.button, (self.s(380), self.s(85)))

            self.font = pygame.font.Font(FONT, self.s(40))

            self.title_font = pygame.font.Font(FONT, self.s(90))

        except (pygame.error, FileNotFoundError):
            print("Error: could not load menu assets")
            self.app.running = False
            return

        # one Rect per button, used to draw AND to detect clicks
        self.button_rects = []
        y = self.y(300)
        for i in range(4):
            rect = self.button.get_rect(midtop=(self.width // 2, y))
            self.button_rects.append(rect)
            y += self.s(80)

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window."""
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window."""
        return self.top + self.s(value)

    def write(self, screen, text, font, color, **position):
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(**position))

    def choose(self, index):
        game_scene = self.app.scenes["game"]
        target = self.options[index]

        if target == "RESUME":
            game_scene.game.resume_game()
            self.app.change_scene("game")
        elif target == "MAIN MENU":
            game_scene.game = None
            self.app.change_scene("menu")
        else:
            self.app.change_scene(target)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(3):
                if self.button_rects[i].collidepoint(event.pos):
                    self.choose(i)

    def draw(self, screen):
        center_x = self.width // 2
        shadow = self.s(4)

        self.app.scenes["game"].draw(screen)

        screen.blit(self.shade, (0, 0))

        self.write(screen, "PAUSED", self.title_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(214)))
        self.write(screen, "PAUSED", self.title_font, (225, 225, 255),
                   center=(center_x, self.y(210)))

        for i in range(2):
            rect = self.button_rects[i]
            screen.blit(self.button, rect)

            text = self.font.render(self.options[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect.move(self.s(12), 0))

    def on_enter(self):
        game = self.app.scenes["game"].game
        if game is not None:
            game.game_paused = True
            game.pause_started_at = time.monotonic()
