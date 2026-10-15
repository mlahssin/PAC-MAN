import pygame
from scenes.base import Scene


class Instructions(Scene):

    def __init__(self, app):
        super().__init__(app)

        config = {"points_per_pacgum": 10, "points_per_super_pacgum": 50,
                  "points_per_ghost": 200, "lives": 3}

        self.rules = [
            ("arrows", "MOVE WITH ARROWS / WASD",
             "Run through the village maze"),
            ("gum", "EAT EVERY GUM",
             f"+{config['points_per_pacgum']} pts - clear them all to win"),
            ("super", "GRAB A SUPER GUM",
             f"+{config['points_per_super_pacgum']} pts - rivals become weak"),
            ("ghost", "HUNT WEAK RIVALS",
             f"+{config['points_per_ghost']} pts - otherwise, run!"),
            ("heart", f"YOU HAVE {config['lives']} LIVES",
             "Touched by a rival = lose one"),
        ]

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
                self.scroll_panel, (470, 500)
            )

            self.panel_w, self.panel_h = self.scroll_panel.get_size()

            self.back_button = pygame.image.load(
                "assets/button.png").convert_alpha()

            self.back_button = pygame.transform.smoothscale(
                self.back_button, (420, 80))

            self.title_font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 10)

            self.big_font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 22)

            self.small_font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 17)

            self.button_font = pygame.font.Font(
                "assets/fonts/Bangers-Regular.ttf", 36)

        except (pygame.error, FileNotFoundError):
            print("Error: could not load menu assets")
            self.app.running = False

        self.icons = {}

        files = {
            "arrows": "assets/icon_arrows.png",
            "gum": "assets/gum.png",
            "super": "assets/supergum.png",
            "ghost": "assets/ghost.png",
            "heart": "assets/lives/full_heart.png"
        }

        for name, path in files.items():
            try:
                icon = pygame.image.load(path).convert_alpha()
                self.icons[name] = pygame.transform.smoothscale(icon, (34, 32))
            except (pygame.error, FileNotFoundError):
                pass

        self.back_rect = self.back_button.get_rect(
            center=(self.width // 2, 635))

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.app.change_scene("menu")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self.app.change_scene("menu")

    def draw(self, screen):

        center_x = self.width // 2

        screen.blit(self.background, (0, 0))

        panel_x = self.width // 2 - self.panel_w // 2
        panel_y = 145

        screen.blit(self.scroll_panel, (panel_x, panel_y))

        y = panel_y + 95
        for icon_name, big, small in self.rules:

            if icon_name in self.icons:
                screen.blit(self.icons[icon_name], (panel_x + 105, y + 6))

            text = self.big_font.render(big, True, (45, 25, 15))
            screen.blit(text, (panel_x + 145, y))

            text = self.small_font.render(small, True, (110, 70, 40))
            screen.blit(text, (panel_x + 145, y + 22))

            y += 70

        screen.blit(self.back_button, self.back_rect)

        label = self.button_font.render("BACK", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=self.back_rect.center))

        hint = self.small_font.render("ESC or ENTER : BACK TO MENU", True, (255, 255, 255))
        screen.blit(hint, hint.get_rect(center=(center_x, 775)))
