from typing import Any

import pygame
from scenes.base import Scene
import time

FONT = "assets/fonts/Bangers-Regular.ttf"

DESIGN_W = 1200
DESIGN_H = 800


class Pause(Scene):
    """Overlay scene shown when the game is paused.

    Renders the game frame underneath a dark shade, then draws
    RESUME and MAIN MENU buttons on top.

    Attributes:
        options: List of button labels.
        width: Window width in pixels.
        height: Window height in pixels.
        scale: Scaling factor from design resolution to window resolution.
        top: Vertical offset to center the design in the window.
        shade: Semi-transparent dark surface used as background overlay.
        button: Button image surface.
        font: Font used for button labels.
        title_font: Larger font used for the PAUSED title.
        button_rects: List of Rect objects for each button.
    """

    def __init__(self, app: Any) -> None:
        """Load images and fonts; create the button rects.

        Args:
            app: The main App object (gives the window and change_scene).
        """
        super().__init__(app)

        self.options = ["RESUME", "MAIN MENU"]

        self.width, self.height = self.app.window.get_size()

        self.scale = min(self.width / DESIGN_W, self.height / DESIGN_H)

        self.top = (self.height - int(DESIGN_H * self.scale)) // 2

        try:
            self.shade = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
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

        self.button_rects = []
        y = self.y(300)
        for i in range(4):
            rect = self.button.get_rect(midtop=(self.width // 2, y))
            self.button_rects.append(rect)
            y += self.s(80)

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

    def choose(self, index: int) -> None:
        """Execute the action for the selected button.

        RESUME resumes the game; MAIN MENU returns to the menu.

        Args:
            index: The button index (0 = RESUME, 1 = MAIN MENU).
        """
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

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dispatch a left click to the relevant button action.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(2):
                if self.button_rects[i].collidepoint(event.pos):
                    self.choose(i)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game frame, dark overlay, title, and buttons.

        Args:
            screen: The window surface to draw on.
        """
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

    def on_enter(self) -> None:
        """Pause the game and record the time when the pause started."""
        game = self.app.scenes["game"].game
        if game is not None:
            game.game_paused = True
            game.pause_started_at = time.monotonic()
