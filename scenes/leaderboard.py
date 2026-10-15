import pygame
from scenes.base import Scene

FONT = "assets/fonts/Bangers-Regular.ttf"
DARK_BROWN = (45, 25, 15)
MID_BROWN = (75, 45, 25)
LIGHT_BROWN = (110, 70, 40)
WHITE = (255, 255, 255)
ICE_BLUE = (120, 220, 255)
MEDALS = [(230, 180, 40), (190, 195, 205), (200, 120, 60)]   # gold, silver, bronze


class Leaderboard(Scene):

    def __init__(self, app):
        super().__init__(app)

        self.width, self.height = self.app.window.get_size()

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
                self.background, (self.width, self.height)
            )

            self.scroll_panel = pygame.image.load(
                "assets/scroll_panel.png").convert_alpha()
            self.scroll_panel = pygame.transform.smoothscale(
                self.scroll_panel, (470, 500)
            )

            self.panel_w, self.panel_h = self.scroll_panel.get_size()

            self.back_button = pygame.image.load(
                "assets/button.png").convert_alpha()

            self.back_button = pygame.transform.smoothscale(
                self.back_button, (420, 80))

            self.title_font = pygame.font.Font(FONT, 80)
            self.subtitle_font = pygame.font.Font(FONT, 26)
            self.header_font = pygame.font.Font(FONT, 15)
            self.row_font = pygame.font.Font(FONT, 18)
            self.button_font = pygame.font.Font(FONT, 40)

        except (pygame.error, FileNotFoundError):
            print("Error: could not load leaderboard assets")
            self.app.running = False
            return

        self.panel_w, self.panel_h = self.scroll_panel.get_size()
        self.back_rect = self.back_button.get_rect(
            center=(self.width // 2, 635))

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

        screen.blit(self.background, (0, 0))

        self.write(screen, "HALL OF SHADOWS", self.title_font, (0, 0, 0),
                   center=(center_x + 4, 64))
        self.write(screen, "HALL OF SHADOWS", self.title_font, WHITE,
                   center=(center_x, 60))
        self.write(screen, "TOP 10 NINJAS", self.subtitle_font, (0, 0, 0),
                   center=(center_x + 4, 114))
        self.write(screen, "TOP 10 NINJAS", self.subtitle_font, WHITE,
                   center=(center_x, 112))

        panel_x = self.width // 2 - self.panel_w // 2
        panel_y = 145

        screen.blit(self.scroll_panel, (panel_x, panel_y))

        left = panel_y + 350
        name_x = left + 50
        right = panel_x + self.panel_w - 130

        y = panel_y + 80
        self.write(screen, "RANK", self.header_font, LIGHT_BROWN, midleft=(left, y))
        self.write(screen, "NAME", self.header_font, LIGHT_BROWN, midleft=(name_x, y))
        self.write(screen, "SCORE", self.header_font, LIGHT_BROWN, midright=(right, y))
        pygame.draw.line(screen, (150, 110, 70), (left, y + 16), (right, y + 16), 2)

        y += 40
        if not self.users:
            self.write(screen, "No ninja has fought yet", self.row_font,
                MID_BROWN, center=(center_x, y+100))

        for i, (name, score) in enumerate(self.users[:10]):

            if i < 3:
                pygame.draw.circle(screen, (60, 35, 20), (left + 18, y), 16)
                pygame.draw.circle(screen, MEDALS[i], (left + 18, y), 14)
                self.write(screen, str(i + 1), self.header_font, DARK_BROWN,
                           center=(left + 18, y + 1))
                color = DARK_BROWN
            else:
                self.write(screen, f"{i + 1}.", self.row_font, LIGHT_BROWN,
                           center=(left + 18, y))
                color = MID_BROWN

            self.write(screen, name, self.row_font, color, midleft=(name_x, y))
            self.write(screen, str(score), self.row_font, color,
                       midright=(right, y))

            y += 35

        screen.blit(self.back_button, self.back_rect)
        self.write(screen, "BACK", self.button_font, WHITE,
                   center=(self.back_rect.centerx + 10, self.back_rect.centery))
