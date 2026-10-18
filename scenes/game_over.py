import pygame
from scenes.base import Scene

FONT = "assets/fonts/Bangers-Regular.ttf"
GAME_OVER_RED = (230, 50, 60)
DARK_BROWN = (45, 25, 15)
LIGHT_BROWN = (110, 70, 40)
WHITE = (255, 255, 255)

# the layout was designed for this window size
DESIGN_W = 1200
DESIGN_H = 800

MAX_NAME = 10


class GameOver(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.width, self.height = self.app.window.get_size()

        # how much bigger than the design: 2100x1500 -> 1.75
        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)
        # empty space left at the top so the layout is centered vertically
        self.top = (self.height - int(DESIGN_H * self.scale)) // 2


        try:
            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (self.width, self.height))

            self.scroll_panel = pygame.image.load(
                "assets/scroll_panel.png").convert_alpha()
            self.scroll_panel = pygame.transform.smoothscale(
                self.scroll_panel, (self.s(470), self.s(500)))

            self.save_button = pygame.image.load(
                "assets/button.png").convert_alpha()
            self.save_button = pygame.transform.smoothscale(
                self.save_button, (self.s(420), self.s(80)))

            self.title_font = pygame.font.Font(FONT, self.s(80))
            self.score_font = pygame.font.Font(FONT, self.s(60))
            self.subtitle_font = pygame.font.Font(FONT, self.s(26))
            self.level_font = pygame.font.Font(FONT, self.s(40))

            self.label_font = pygame.font.Font(FONT, self.s(26))
            self.name_font = pygame.font.Font(FONT, self.s(40))

            self.name_box = pygame.Rect(0, 0, self.s(250), self.s(58))
            self.name_box.center = (self.width // 2, self.y(500))

            self.name = ""

            self.button_font = pygame.font.Font(FONT, self.s(40))

        except (pygame.error, FileNotFoundError):
            print("Error: could not load leaderboard assets")
            self.app.running = False
            return

        self.panel_w, self.panel_h = self.scroll_panel.get_size()
        self.back_rect = self.save_button.get_rect(
            center=(self.width // 2, self.y(635)))

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window."""
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window."""
        return self.top + self.s(value)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                letter = event.unicode
                if (len(letter) == 1 and (letter.isalnum() or letter == " ")) and len(self.name) < MAX_NAME:
                    self.name += letter.upper()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.save_name()

    def write(self, screen, text, font, color, **position):
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(**position))

    def save_name(self):

        self.name = self.name.strip()

        if self.name == "":
            return

        print(f"SAVE: {self.name}")
        self.app.change_scene("menu")

    def draw(self, screen):
        center_x = self.width // 2
        shadow = self.s(4)

        screen.blit(self.background, (0, 0))

        # title + subtitle (black copy shifted = shadow)
        self.write(screen, "GAME OVER", self.title_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(64)))
        self.write(screen, "GAME OVER", self.title_font, GAME_OVER_RED,
                   center=(center_x, self.y(60)))
        self.write(screen, "THE SHADOWS CAUGHT YOU...", self.subtitle_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(114)))
        self.write(screen, "THE SHADOWS CAUGHT YOU...", self.subtitle_font, WHITE,
                   center=(center_x, self.y(112)))

        # scroll
        panel_x = center_x - self.panel_w // 2
        panel_y = self.y(145)
        screen.blit(self.scroll_panel, (panel_x, panel_y))

        level = self.app.last_level
        score = self.app.last_score

        self.write(screen, "FINAL SCORE", self.subtitle_font, LIGHT_BROWN,
                   center=(center_x, self.y(235)))

        self.write(screen, f"{score:02d}", self.score_font, DARK_BROWN,
                   center=(center_x, self.y(275)))

        self.write(screen, "LEVEL", self.subtitle_font, LIGHT_BROWN,
                   center=(center_x, self.y(350)))

        self.write(screen, f"{level:02d} / 10", self.level_font, DARK_BROWN,
                   center=(center_x, self.y(380)))

        self.write(screen, "Enter your name", self.label_font, LIGHT_BROWN,
                   center=(center_x, self.y(455)))

        pygame.draw.rect(screen, (250, 240, 220), self.name_box, 0, self.s(10))
        pygame.draw.rect(screen, (40, 120, 190), self.name_box, max(1, self.s(3)), self.s(10))

        text = self.name_font.render(self.name, True, DARK_BROWN)
        text_rect = text.get_rect(
            midleft=(self.name_box.left + self.s(18), self.name_box.centery + self.s(2))
        )
        screen.blit(text, text_rect)

        # back button
        screen.blit(self.save_button, self.back_rect)
        self.write(screen, "SAVE", self.button_font, WHITE,
                   center=(self.back_rect.centerx + self.s(10),
                           self.back_rect.centery))
