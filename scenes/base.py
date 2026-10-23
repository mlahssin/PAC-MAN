from typing import Any
import pygame


class Scene:
    """Abstract base for all game scenes.

    Subclasses override on_enter, handle_event, update, and draw.

    Attributes:
        app: The main App instance that owns this scene.
    """

    def __init__(self, app: Any) -> None:
        """Store the app reference.

        Args:
            app: The main App object.
        """
        self.app = app

    def on_enter(self) -> None:
        """Called once when the scene becomes the active scene."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle.
        """
        pass

    def update(self, dt: float) -> None:
        """Advance the scene's state by one frame.

        Args:
            dt: Milliseconds elapsed since the last frame.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Render the scene to the window surface.

        Args:
            screen: The window surface to draw on.
        """
        pass
