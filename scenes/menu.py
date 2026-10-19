"""Main menu scene: PLAY, INSTRUCTIONS, LEADERBOARD and QUIT."""

import pygame
from scenes.base import Scene


DESIGN_W = 1200
DESIGN_H = 800


class MenuScene(Scene):
    """First screen of the game, with one button per option.

    A left click on a button opens its scene, or quits the game.
    """

    def __init__(self, app):
        """Load the background, the button image and the font.

        Args:
            app: The main App object (gives the window and change_scene).
        """
        super().__init__(app)

        self.options = ["PLAY", "INSTRUCTIONS", "LEADERBOARD", "QUIT"]
        self.scenes = ["game", "instructions", "leaderboard", "quit"]

        width, height = self.app.window.get_size()

        self.scale = min(width / DESIGN_W, height / DESIGN_H)
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

        except (pygame.error, OSError):
            print("Error: could not load menu assets")
            self.app.running = False
            return

        self.button_rects = []
        y = self.y(400)
        for i in range(4):
            rect = self.button.get_rect(midtop=(width // 2, y))
            self.button_rects.append(rect)
            y += self.s(80)

    def s(self, value):
        """Scale a size from the 1200x800 design to the real window.

        Args:
            value: A size in the 1200x800 design.

        Returns:
            The same size in real window pixels.
        """
        return int(value * self.scale)

    def y(self, value):
        """Scale a vertical position from the design to the real window.

        Args:
            value: A y position in the 1200x800 design.

        Returns:
            The y position in the real window (centered vertically).
        """
        return self.top + self.s(value)

    def choose(self, index):
        """Open the scene of the clicked button, or quit the game.

        PLAY always starts a new game.

        Args:
            index: The position of the button (0 = PLAY, 3 = QUIT).
        """
        target = self.scenes[index]
        if target == "quit":
            self.app.running = False
        else:
            print(target)
            self.app.change_scene(target)

    def handle_event(self, event):
        """Check if a button was clicked with the left mouse button.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(4):
                if self.button_rects[i].collidepoint(event.pos):
                    self.choose(i)

    def draw(self, screen):
        """Draw the background and every button with its text.

        Args:
            screen: The window surface to draw on.
        """
        screen.blit(self.background, (0, 0))

        for i in range(4):
            rect = self.button_rects[i]
            screen.blit(self.button, rect)

            text = self.font.render(self.options[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect.move(self.s(12), 0))
