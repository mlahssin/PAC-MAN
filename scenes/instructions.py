import pygame
from scenes.base import Scene

# the layout was designed for this window size
DESIGN_W = 1200
DESIGN_H = 800


class Instructions(Scene):

    def __init__(self, app):
        super().__init__(app)

        config = {"points_per_pacgum": 10, "points_per_super_pacgum": 50, "points_per_ghost": 200, "lives": 3, "level_max_time": 90}

        self.rules = [
            ("arrows", "MOVE WITH ARROWS / WASD",
             "P or ESC to pause"),
            ("gum", "EAT EVERY GUM",
             f"+{config['points_per_pacgum']} pts - clear them all to finish the level"),
            ("super", "GRAB A SUPER GUM",
             f"+{config['points_per_super_pacgum']} pts - rivals are weak for a short time"),
            ("ghost", "HUNT WEAK RIVALS",
             f"+{config['points_per_ghost']} pts - otherwise, run!"),
            ("heart", f"YOU HAVE {config['lives']} LIVES",
             "touched by a rival = lose one, back to the center"),
            ("time", "BEAT THE CLOCK",
             f"{config['level_max_time']} s per level - finish 10 levels to win"),
        ]

        self.width, self.height = self.app.window.get_size()

        # how much bigger than the design: 2100x1500 -> 1.75
        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)
        # empty space left at the top so the layout is centered vertically
        self.top = (self.height - int(DESIGN_H * self.scale)) // 2

        font = "assets/fonts/Bangers-Regular.ttf"

        try:
            self.background = pygame.image.load(
                "assets/menu_background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (self.width, self.height))

            self.scroll_panel = pygame.image.load(
                "assets/scroll_panel.png").convert_alpha()
            self.scroll_panel = pygame.transform.smoothscale(
                self.scroll_panel, (self.s(600), self.s(500)))

            self.panel_w, self.panel_h = self.scroll_panel.get_size()

            self.back_button = pygame.image.load(
                "assets/button.png").convert_alpha()
            self.back_button = pygame.transform.smoothscale(
                self.back_button, (self.s(420), self.s(80)))

            self.title_font = pygame.font.Font(font, self.s(80))
            self.big_font = pygame.font.Font(font, self.s(22))
            self.small_font = pygame.font.Font(font, self.s(16))
            self.button_font = pygame.font.Font(font, self.s(36))

        except (pygame.error, FileNotFoundError):
            print("Error: could not load instructions assets")
            self.app.running = False
            return

        self.icons = {}
        files = {
            "arrows": "assets/icon_arrows.png",
            "gum": "assets/gum.png",
            "super": "assets/supergum.png",
            "ghost": "assets/ghost.png",
            "heart": "assets/lives/full_heart.png",
            "time": "assets/clock.png",
        }
        for name, path in files.items():
            try:
                icon = pygame.image.load(path).convert_alpha()
                # if 
                self.icons[name] = pygame.transform.smoothscale(
                    icon, (self.s(34), self.s(33)))
            except (pygame.error, FileNotFoundError):
                print(f"Warning: icon '{name}' not found at {path}")

        self.back_rect = self.back_button.get_rect(
            center=(self.width // 2, self.y(635)))

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window."""
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window."""
        return self.top + self.s(value)

    def write(self, screen, text, font, color, **position):
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(**position))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.app.change_scene("menu")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.app.change_scene("menu")

    def draw(self, screen):
        center_x = self.width // 2
        shadow = self.s(4)

        screen.blit(self.background, (0, 0))

        self.write(screen, "INSTRUCTIONS", self.title_font, (0, 0, 0),
                   center=(center_x + shadow, self.y(64)))
        self.write(screen, "INSTRUCTIONS", self.title_font, (255, 255, 255),
                   center=(center_x, self.y(60)))

        panel_x = center_x - self.panel_w // 2
        panel_y = self.y(145)
        screen.blit(self.scroll_panel, (panel_x, panel_y))

        y = panel_y + self.s(95)
        for icon_name, big, small in self.rules:

            if icon_name in self.icons:
                screen.blit(self.icons[icon_name],
                            (panel_x + self.s(140), y + self.s(6)))

            text = self.big_font.render(big, True, (45, 25, 15))
            screen.blit(text, (panel_x + self.s(185), y))

            text = self.small_font.render(small, True, (110, 70, 40))
            screen.blit(text, (panel_x + self.s(185), y + self.s(22)))

            y += self.s(60)

        screen.blit(self.back_button, self.back_rect)

        label = self.button_font.render("BACK", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=self.back_rect.center))

        hint = self.small_font.render("ESC or ENTER : BACK TO MENU",
                                      True, (255, 255, 255))
        screen.blit(hint, hint.get_rect(center=(center_x, self.y(775))))
