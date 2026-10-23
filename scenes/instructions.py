from typing import Any

import pygame
from scenes.base import Scene

DESIGN_W = 1200
DESIGN_H = 800


class Instructions(Scene):
    """Screen that shows the game rules on a scroll, with a BACK button.

    Each rule has an icon, a title and a short explanation.
    """

    def __init__(self, app: Any) -> None:
        """Build the rules, load the images, fonts and icons.

        If a main image or font is missing, the game stops cleanly.
        If only an icon is missing, the rule is drawn without it.

        Args:
            app: The main App object (gives the window and change_scene).
        """
        super().__init__(app)

        config = {
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "lives": 3,
            "level_max_time": 90,
        }

        self.rules = [
            ("arrows", "MOVE WITH ARROWS / WASD",
                "P or ESC to pause"),
            (
                "gum",
                "EAT EVERY GUM",
                f"+{config['points_per_pacgum']} pts - "
                "clear them all to finish the level",
            ),
            (
                "super",
                "GRAB A SUPER GUM",
                f"+{config['points_per_super_pacgum']} pts - "
                "rivals are weak for a short time",
            ),
            (
                "ghost",
                "HUNT WEAK RIVALS",
                f"+{config['points_per_ghost']} pts - otherwise, run!",
            ),
            (
                "heart",
                f"YOU HAVE {config['lives']} LIVES",
                "touched by a rival = lose one, back to the center",
            ),
            (
                "time",
                "BEAT THE CLOCK",
                f"{config['level_max_time']} s per level - "
                "finish 10 levels to win",
            ),
        ]

        self.width, self.height = self.app.window.get_size()

        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)
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

        except (pygame.error, OSError):
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
                self.icons[name] = pygame.transform.smoothscale(
                    icon, (self.s(34), self.s(33)))
            except (pygame.error, OSError):
                print(f"Warning: icon '{name}' not found at {path}")

        self.back_rect = self.back_button.get_rect(
            center=(self.width // 2, self.y(635)))

    def s(self, value: int) -> int:
        """Scale a size from the 1200x800 design to the real window.

        Args:
            value: A size in the 1200x800 design.

        Returns:
            The same size in real window pixels.
        """
        return int(value * self.scale)

    def y(self, value: int) -> int:
        """Scale a vertical position from the design to the real window.

        Args:
            value: A y position in the 1200x800 design.

        Returns:
            The y position in the real window (centered vertically).
        """
        return int(self.top) + self.s(value)

    def write(self, screen: pygame.Surface, text: str,
              font: pygame.font.Font, color: tuple[int, int, int],
              **position: Any) -> None:
        """Draw a text on the screen at a given position.

        Args:
            screen: The surface to draw on.
            text: The text to draw.
            font: The pygame font to use.
            color: The text color (R, G, B).
            **position: A Rect anchor, for example center=(x, y).
        """
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(**position))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Go back to the menu with ESC, ENTER or a click on BACK.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.app.change_scene("menu")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_rect.collidepoint(event.pos):
                self.app.change_scene("menu")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the title, the scroll with all the rules, and BACK.

        Args:
            screen: The window surface to draw on.
        """
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
