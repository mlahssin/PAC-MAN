from __future__ import annotations
from maze import Maze
from Character import Player, Ghost
import time
import random


CELL = 80


class Game:
    """Manage game state, levels, entities, and gameplay rules.

    Attributes:
        width: Number of maze columns.
        height: Number of maze rows.
        seed: Base seed (first level uses this value).
        start: Center grid cell (x, y) where the player spawns.
        start_pix: Pixel coordinates of the player spawn point.
        corners: List of the four corner cells used for ghost spawns.
        lives: Remaining player lives.
        score: Current accumulated score.
        stop: Legacy flag (unused in current code).
        level: Current level number (1-based).
        levels_frames: Frames-per-cell for each level (lower = faster).
        speed_boost_active: True while the cheat speed boost is active.
        random_per: Random-move coefficient per level for ghosts.
        cheat_mode: True when cheat mode is enabled.
        invincible: True when the player cannot lose lives.
        ghosts_frozen_active: True while ghosts are frozen by a cheat.
        level_normal_time: Default time limit in seconds for each level.
        pass_level_active: True while a level-skip cheat is active.
        levels_seeds: Fixed seeds for each of the 10 levels.
        game_over: True when the game has ended in defeat.
        game_won: True when all 10 levels have been cleared.
        pacgum_points: Points awarded per regular gum collected.
        supergum_points: Points awarded per supergum collected.
        ed_ghost_points: Points awarded per edible ghost eaten.
    """

    def __init__(
        self,
        width: int = 15,
        height: int = 15,
        perfect: bool = False,
        seed: int = 42,
    ) -> None:
        """Initialize game settings and prepare the first level.

        Args:
            width: Number of maze columns. Defaults to 15.
            height: Number of maze rows. Defaults to 15.
            perfect: True for a perfect maze, False for imperfect.
                Defaults to False.
            seed: Random seed for the first level. Defaults to 42.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.start = (width // 2, height // 2)

        self.start_pix = (
            ((width // 2) * CELL) + CELL // 2,
            (height // 2) * CELL + CELL // 2
        )

        self.corners: list[tuple[int, int]] = [
            (0, 0),
            (width - 1, height - 1),
            (width - 1, 0),
            (0, height - 1)
        ]

        self.lives = 3
        self.score = 0
        self.stop = False

        self.level = 1
        self.levels_frames = [
            24, 24, 22, 22, 20, 20, 18, 18, 16, 16
        ]

        self.speed_boost_active = False
        self.random_per = [3, 4, 5, 6, 7, 8, 9, 10, 20, 100]
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen_active = False
        self.level_normal_time = 180
        self.pass_level_active = False
        # self.levels_seeds = [42, 14, 26, 39, 52, 78, 71, 84, 93, 11]
        self.levels_seeds = [42] + [
            random.randint(0, 1_000_000) for _ in range(9)
        ]

        self.pacgum_points = 10
        self.supergum_points = 50
        self.ed_ghost_points = 200

        self.initialize_level()

        self.game_over = False
        self.game_won = False

    def initialize_level(self) -> None:
        """Generate the maze and initialize entities and level state."""

        self.maze = Maze(
            self.width,
            self.height,
            False,
            self.levels_seeds[self.level - 1]
        )

        self.grid = self.maze.grid
        self.player = Player(
            (self.width // 2, self.height // 2),
            None
        )

        self.player.requested_direction = None
        self.player.direction = None
        self.player.target_pos = None
        self.player.previous_pos = None

        self.ghosts = [
            Ghost((0, 0), None),
            Ghost((self.width - 1, self.height - 1), None),
            Ghost((self.width - 1, 0), None),
            Ghost((0, self.height - 1), None)
        ]

        self.coeficient = 4

        for ghost in self.ghosts:
            ghost.start_pos = ghost.pos
            ghost.frames_per_cell = self.levels_frames[self.level - 1]
            ghost.coefecient = self.random_per[self.level - 1]

        self.gums = self.gums_placement()
        self.super_gums = self.super_gum()
        self.edible_active_unitl = 0.0
        self.visited: set[tuple[int, int]] = set()
        self.level_completed = False
        self.level_expires_at = time.monotonic() + self.level_normal_time
        self.game_paused = False
        self.pause_started_at: float | None = None

    def gums_placement(self) -> set[tuple[int, int]]:
        """Place gums in reachable cells excluding spawn positions.

        Returns:
            A set of (x, y) tuples where a gum should appear.
        """
        gums: set[tuple[int, int]] = set()

        reachable = self.maze.get_reachable_cells(self.start)

        for i in range(self.width):
            for item in range(self.height):
                cell = (i, item)

                if (
                    cell in reachable
                    and cell not in self.corners
                    and cell != self.start
                ):
                    gums.add(cell)

        return gums

    def super_gum(self) -> set[tuple[int, int]]:
        """Place supergums at the four maze corners.

        Returns:
            A set of (x, y) tuples for the four corner positions.
        """
        return set(self.corners)

    def does_level_completed(self) -> bool:
        """Check whether the level is completed or its timer has expired.

        Returns:
            True if all gums are collected or time ran out, False otherwise.
        """
        if not self.gums and not self.super_gums:
            self.level_completed = True
            return True
        elif time.monotonic() >= self.level_expires_at:
            self.level_completed = True
            return True
        return False

    def succesfully_complete_level(self) -> bool:
        """Check whether all gums and supergums have been collected.

        Returns:
            True if both gum sets are empty, False otherwise.
        """
        if not self.gums and not self.super_gums:
            return True
        return False

    def Next_level(self) -> None:
        """Advance to the next level or finish the game."""
        if not self.game_over:
            self.level += 1

            if self.level > 10:
                self.game_won = True
                self.game_over = True
                self.level -= 1
                return

            self.initialize_level()

    def collect_gums(self) -> None:
        """Collect gums and activate edible mode when appropriate."""

        if self.player.target_pos is not None:
            return

        if self.player.pos not in self.visited:
            if self.player.pos in self.gums:
                self.score += self.pacgum_points
                self.visited.add(self.player.pos)
                self.gums.remove(self.player.pos)

            elif self.player.pos in self.super_gums:
                self.score += self.supergum_points
                self.visited.add(self.player.pos)
                self.super_gums.remove(self.player.pos)

                for g in self.ghosts:
                    g.state = "EDIBLE"

                self.edible_active_unitl = time.monotonic() + 100

    def detect_collision(self) -> Ghost | None:
        """Return the first ghost colliding with the player, if any.

        Returns:
            The Ghost instance that collides with the player, or None.
        """
        for g in self.ghosts:
            dx = self.player.x_pix - g.x_pix
            dy = self.player.y_pix - g.y_pix

            collision = dx * dx + dy * dy <= (20 + 20) ** 2

            if collision:
                return g

        return None

    def handle_collisions(self) -> None:
        """Handle collisions according to the ghost's current state."""
        g = self.detect_collision()

        if g is not None:
            if g.state == "DANGEROUS":

                if not self.invincible:
                    self.lives -= 1

                    if self.lives == 0:
                        self.game_over = True
                        return
                    self.player.pos = self.start
                    self.player.target_pos = None
                    self.player.direction = None
                    self.player.requested_direction = None
                    self.player.previous_pos = None

                    self.player.x_pix = (
                        self.player.pos[0] * CELL + CELL / 2
                    )
                    self.player.y_pix = (
                        self.player.pos[1] * CELL + CELL / 2
                    )

                    for i, gos in enumerate(self.ghosts):
                        gos.pos = self.corners[i]
                        gos.x_pix = gos.pos[0] * CELL + CELL / 2
                        gos.y_pix = gos.pos[1] * CELL + CELL / 2
                        gos.target_pos = None
                        gos.direction = None
                        gos.previous_pos = None
                        gos.state = "DANGEROUS"
                        gos.respawn_time_at = 0.0

                    self.edible_active_unitl = 0.0

            elif g.state == "EDIBLE":
                assert g.start_pos is not None
                g.pos = g.start_pos
                g.x_pix = g.pos[0] * CELL + CELL / 2
                g.y_pix = g.pos[1] * CELL + CELL / 2
                g.target_pos = None
                g.direction = None
                g.previous_pos = None
                g.state = "RESPAWNING"
                g.respawn_time_at = time.monotonic() + 10

                self.score += self.ed_ghost_points

            elif g.state == "RESPAWNING":
                pass

    def ghost_update(self) -> None:
        """Update edible and respawning ghost states when timers expire."""
        now = time.monotonic()

        if self.edible_active_unitl and now >= self.edible_active_unitl:
            for gost in self.ghosts:
                if gost.state == "EDIBLE":
                    gost.state = "DANGEROUS"

            self.edible_active_unitl = 0.0

        for g in self.ghosts:
            if (
                g.state == "RESPAWNING"
                and g.respawn_time_at
                and now >= g.respawn_time_at
            ):
                g.respawn_time_at = 0.0
                g.state = "DANGEROUS"

    def pause_option(self) -> None:
        """Pause the game and record the pause start time."""
        self.game_paused = True
        self.pause_started_at = time.monotonic()

    def resume_game(self) -> None:
        """Resume the game and compensate for elapsed pause time."""
        self.game_paused = False
        assert self.pause_started_at is not None
        paused_time = time.monotonic() - self.pause_started_at

        self.level_expires_at += paused_time

        if self.edible_active_unitl:
            self.edible_active_unitl += paused_time

        for g in self.ghosts:
            if g.state == "RESPAWNING":
                g.respawn_time_at += paused_time

        self.game_paused = False
        self.pause_started_at = None

    def switch_to_cheat_mode(self) -> None:
        """Enable cheat mode."""
        self.cheat_mode = True

    def switch_to_normal_mode(self) -> None:
        """Disable cheat mode and reset active cheat effects."""
        self.cheat_mode = False
        self.invincible = False
        self.speed_boost_active = False
        self.speed_boost()
        self.ghosts_frozen_active = False
        self.pass_level_active = False

    def iron_man(self) -> None:
        """Toggle player invincibility when cheat mode is enabled."""
        if self.cheat_mode:
            self.invincible = not self.invincible

    def add_life(self) -> None:
        """Add one life when cheat mode is enabled."""
        if self.cheat_mode:
            if self.lives < 3:
                self.lives += 1

    def speed_boost(self) -> None:
        """Toggle or reset the player's movement speed boost."""
        if self.cheat_mode:
            self.speed_boost_active = not self.speed_boost_active

        if self.speed_boost_active:
            self.player.frames_per_cell = max(
                1,
                self.player.normal_frames_per_cell // 2
            )
        else:
            self.player.frames_per_cell = (
                self.player.normal_frames_per_cell
            )

    def ghost_freeze(self) -> None:
        """Toggle ghost freezing when cheat mode is enabled."""
        if self.cheat_mode:
            self.ghosts_frozen_active = not self.ghosts_frozen_active

    def skip_level(self) -> None:
        """Skip the current level when cheat mode is enabled."""
        if self.cheat_mode:
            self.Next_level()
