from __future__ import annotations
import pygame
from scenes.game import GameScene
from scenes.menu import MenuScene
from scenes.game_over import GameOver
from scenes.victory import Victory
from scenes.pause import Pause
from scenes.instructions import Instructions
from scenes.leaderboard import Leaderboard
from Leaderboard import Leaderboard_Engine
from config import Settings


class App:
    """Main application: owns the window, the clock, and all scenes.

    Attributes:
        window: The pygame display surface.
        clock: The pygame clock used to cap the frame rate.
        running: False stops the main loop.
        fps: Target frames per second.
        settings: The game settings loaded from the config file.
        last_score: Score recorded at the end of the last game.
        last_level: Level reached at the end of the last game.
        leadearboard: The persistent high-score engine.
        scenes: Dict mapping scene names to their Scene instances.
        current_scene: The scene currently being updated and drawn.
    """

    def __init__(self, width: int, height: int, settings: Settings) -> None:
        """Set up pygame, the window, and all scenes.

        Args:
            width: Window width in pixels.
            height: Window height in pixels.
            settings: A Settings instance from the config file.
        """
        pygame.init()
        pygame.display.set_caption("PAC MAN")

        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        self.settings = settings

        self.last_score = 0
        self.last_level = 1

        self.leadearboard = Leaderboard_Engine()

        self.scenes = {
            "game": GameScene(self),
            "menu": MenuScene(self),
            "instructions": Instructions(self),
            "leaderboard": Leaderboard(self),
            "game_over": GameOver(self),
            "victory": Victory(self),
            "pause": Pause(self)
        }

        self.current_scene = self.scenes["menu"]
        self.current_scene.on_enter()

    def change_scene(self, scene: str) -> None:
        """Switch to a different scene and call its on_enter hook.

        Args:
            scene: The name key of the target scene.
        """
        self.current_scene = self.scenes[scene]
        self.current_scene.on_enter()

    def run(self) -> None:
        """Run the main game loop until the window is closed."""

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_scene.handle_event(event)

            dt = self.clock.tick(self.fps)
            self.current_scene.update(dt)
            self.current_scene.draw(self.window)
            pygame.display.flip()

        pygame.quit()
