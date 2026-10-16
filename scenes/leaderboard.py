import pygame
from scenes.base import Scene

FONT = "assets/fonts/Bangers-Regular.ttf"
DARK_BROWN = (45, 25, 15)
MID_BROWN = (75, 45, 25)
LIGHT_BROWN = (110, 70, 40)
WHITE = (255, 255, 255)
ICE_BLUE = (120, 220, 255)
MEDALS = [(230, 180, 40), (190, 195, 205), (200, 120, 60)]   # gold, silver, bronze

# the layout was designed for this window size
DESIGN_W = 1200
DESIGN_H = 800


class Leaderboard(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.width, self.height = self.app.window.get_size()

        # how much bigger than the design: 2100x1500 -> 1.75
        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)
        # empty space left at the top so the layout is centered vertically
        self.top = (self.height - int(DESIGN_H * self.scale)) // 2

        self.users = [
            ("9azdou7", 48250),
            ("AYOUB", 41980),
            ("MOAAD", 39500),
            ("KAGE 42", 27110),
            ("RAIN", 19870),
            ("TSUKI", 15420),
            ("KUNAI", 12030),
            ("NIGHTOWL", 9800),
            ("ZEN", 6450),
            ("PLAYER", 2100),
        ]

        try:
            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (self.width, self.height))

            self.scroll_panel = pygame.image.load(
                "assets/scroll_panel.png").convert_alpha()
            self.scroll_panel = pygame.transform.smoothscale(
                self.scroll_panel, (self.s(470), self.s(500)))

            self.back_button = pygame.image.load(
                "assets/button.png").convert_alpha()
            self.back_button = pygame.transform.smoothscale(
                self.back_button, (self.s(420), self.s(80)))

            self.title_font = pygame.font.Font(FONT, self.s(80))
            self.subtitle_font = pygame.font.Font(FONT, self.s(26))
            self.header_font = pygame.font.Font(FONT, self.s(15))
            self.row_font = pygame.font.Font(FONT, self.s(18))
            self.button_font = pygame.font.Font(FONT, self.s(40))

        except (pygame.error, FileNotFoundError):
            print("Error: could not load leaderboard assets")
            self.app.running = False
            return

        self.panel_w, self.panel_h = self.scroll_panel.get_size()
        self.back_rect = self.back_button.get_rect(
            center=(self.width // 2, self.y(635)))

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window."""
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window."""
        return self.top + self.s(value)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.app.change_scene("menu")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.app.change_scene("menu")

    def write(self, screen, text, font, color, **position):
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(**position))

    def draw(self, screen):
        center_x = self.width // 2
        shadow = self.s(4)

        screen.blit(self.background, (0, 0))

        # title + subtitle (black copy shifted = shadow)
        self.write(screen, "HALL OF SHADOWS", self.title_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(64)))
        self.write(screen, "HALL OF SHADOWS", self.title_font, WHITE,
                   center=(center_x, self.y(60)))
        self.write(screen, "TOP 10 NINJAS", self.subtitle_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(114)))
        self.write(screen, "TOP 10 NINJAS", self.subtitle_font, WHITE,
                   center=(center_x, self.y(112)))

        # scroll
        panel_x = center_x - self.panel_w // 2
        panel_y = self.y(145)
        screen.blit(self.scroll_panel, (panel_x, panel_y))

        # columns
        left = panel_x + self.s(130)          # rank
        name_x = left + self.s(50)            # name
        right = panel_x + self.panel_w - self.s(130)   # score (right edge)

        # header
        y = panel_y + self.s(80)
        self.write(screen, "RANK", self.header_font, LIGHT_BROWN, midleft=(left, y))
        self.write(screen, "NAME", self.header_font, LIGHT_BROWN, midleft=(name_x, y))
        self.write(screen, "SCORE", self.header_font, LIGHT_BROWN, midright=(right, y))
        line_y = y + self.s(16)
        pygame.draw.line(screen, (150, 110, 70), (left, line_y), (right, line_y),
                         max(1, self.s(2)))

        # rows
        y += self.s(40)
        if not self.users:
            self.write(screen, "No ninja has fought yet", self.row_font,
                       MID_BROWN, center=(center_x, y + self.s(100)))

        medal_x = left + self.s(18)
        for i, (name, score) in enumerate(self.users[:10]):

            if i < 3:
                pygame.draw.circle(screen, (60, 35, 20), (medal_x, y), self.s(16))
                pygame.draw.circle(screen, MEDALS[i], (medal_x, y), self.s(14))
                self.write(screen, str(i + 1), self.header_font, DARK_BROWN,
                           center=(medal_x, y + self.s(1)))
                color = DARK_BROWN
            else:
                self.write(screen, f"{i + 1}.", self.row_font, LIGHT_BROWN,
                           center=(medal_x, y))
                color = MID_BROWN

            self.write(screen, name, self.row_font, color, midleft=(name_x, y))
            self.write(screen, str(score), self.row_font, color,
                       midright=(right, y))

            y += self.s(35)

        # back button
        screen.blit(self.back_button, self.back_rect)
        self.write(screen, "BACK", self.button_font, WHITE,
                   center=(self.back_rect.centerx + self.s(10),
                           self.back_rect.centery))
