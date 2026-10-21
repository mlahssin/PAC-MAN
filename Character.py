from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze import Maze

DANGEROUS = "DANGEROUS"
EDIBLE = "EDIBLE"
RESPAWNING = "RESPAWNING"

CELL = 80

pixel_step = CELL / 10

opposite = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

modes = {DANGEROUS, EDIBLE, RESPAWNING}

DIRECTIONS = {
    "up": (0, -1, 1, 4),
    "down": (0, 1, 4, 1),
    "left": (-1, 0, 8, 2),
    "right": (1, 0, 2, 8),
}


class Character:
    """Represent a character with grid-based and pixel-based movement.

    Attributes:
        pos: Current grid cell as a (x, y) tuple.
        direction: Current movement direction string, or None.
        x_pix: Horizontal pixel position (center of the current
            or target cell).
        y_pix: Vertical pixel position (center of the current
            or target cell).
        normal_frames_per_cell: Default number of frames to cross one cell.
        frames_per_cell: Active frames-per-cell (may differ
            during speed boost).
        target_pos: Grid cell the character is moving toward, or None.
        moves: Total number of completed cell crossings.
        previous_pos: Grid cell occupied before the last completed move.
    """

    def __init__(
        self, pos: tuple[int, int], direction: str | None
    ) -> None:
        """Initialize the character's position, direction, and movement.

        Args:
            pos: A (x, y) tuple of integers for the starting grid position.
            direction: Initial direction string, or None.

        Raises:
            TypeError: If pos is not a tuple of two integers.
            ValueError: If direction is not a valid direction string or None.
        """
        if (
            not isinstance(pos, tuple)
            or len(pos) != 2
            or not isinstance(pos[0], int)
            or not isinstance(pos[1], int)
        ):
            raise TypeError("pos must be a tuple of two integers (x, y)")

        if direction is not None and direction not in DIRECTIONS:
            raise ValueError("direction must be None or a valid direction")

        self.pos = pos
        self.direction = direction

        self.x_pix = (pos[0] * CELL) + CELL / 2
        self.y_pix = (pos[1] * CELL) + CELL / 2

        self.normal_frames_per_cell = 20
        self.frames_per_cell = self.normal_frames_per_cell

        self.target_pos: tuple[int, int] | None = None
        self.moves = 0
        self.previous_pos: tuple[int, int] | None = None

    def start_move(self, maze: Maze) -> bool:
        """Start moving toward the next accessible cell.

        Args:
            maze: The Maze instance used to check wall collisions.

        Returns:
            True if a move was started, False if already moving or blocked.
        """
        if self.target_pos is not None:
            return False

        if self.direction is None:
            return False

        if not maze.can_move(self.pos, self.direction):
            return False

        direction = DIRECTIONS[self.direction]

        dx, dy = direction[0], direction[1]
        x, y = self.pos

        self.target_pos = (x + dx, y + dy)
        return True

    def update(self, maze: Maze) -> bool:
        """Update pixel movement and finalize completed cell transitions.

        Args:
            maze: The Maze instance used to start a new move when needed.

        Returns:
            True if movement occurred, False if there was nothing to update.
        """

        if self.target_pos is None:
            if self.direction is None:
                return False

            self.start_move(maze)

            if self.target_pos is None:
                return False

        target_x, target_y = self.target_pos

        target_x_pix = target_x * CELL + CELL / 2
        target_y_pix = target_y * CELL + CELL / 2

        x, y = self.pos

        current_x_pix = x * CELL + CELL / 2
        current_y_pix = y * CELL + CELL / 2

        x_step = (target_x_pix - current_x_pix) / self.frames_per_cell
        y_step = (target_y_pix - current_y_pix) / self.frames_per_cell

        self.x_pix += x_step
        self.y_pix += y_step

        if (
            (x_step > 0 and self.x_pix >= target_x_pix)
            or (x_step < 0 and self.x_pix <= target_x_pix)
        ):
            self.x_pix = target_x_pix

        if (
            (y_step > 0 and self.y_pix >= target_y_pix)
            or (y_step < 0 and self.y_pix <= target_y_pix)
        ):
            self.y_pix = target_y_pix

        if self.x_pix == target_x_pix and self.y_pix == target_y_pix:
            self.previous_pos = self.pos
            self.pos = target_x, target_y
            self.moves += 1
            self.target_pos = None

        return True


class Player(Character):
    """Represent the player and manage requested movement directions.

    Attributes:
        requested_direction: The direction queued by the last
            key press, or None.
    """

    def __init__(
        self, pos: tuple[int, int], direction: str | None
    ) -> None:
        """Initialize the player with no pending direction request.

        Args:
            pos: A (x, y) tuple of integers for the starting grid position.
            direction: Initial direction string, or None.
        """
        super().__init__(pos, direction)
        self.requested_direction: str | None = None

    def request_direction(self, direction: str) -> None:
        """Validate and store the player's requested direction.

        Args:
            direction: One of 'up', 'down', 'left', 'right'.

        Raises:
            TypeError: If direction is not a string.
            ValueError: If direction is not a valid direction.
        """
        if not isinstance(direction, str):
            raise TypeError("direction must be a string")

        direction = direction.lower()

        if direction not in DIRECTIONS:
            raise ValueError("direction must be up, down, left, or right")

        self.requested_direction = direction

    def choose_direction(self, maze: Maze) -> None:
        """Apply the requested direction when movement allows it.

        Args:
            maze: The Maze instance used to check if the move is valid.
        """
        if self.requested_direction is None:
            return

        if self.target_pos is not None:
            if self.direction == opposite[self.requested_direction]:
                self.pos, self.target_pos = self.target_pos, self.pos
                self.direction = self.requested_direction
            return

        if maze.can_move(self.pos, self.requested_direction):
            self.direction = self.requested_direction


class Ghost(Character):
    """Represent a ghost with chasing, fleeing, and respawning behavior.

    Attributes:
        spawn_pos: The corner cell the ghost returns to after being eaten.
        state: Current behavioral state: 'DANGEROUS', 'EDIBLE',
            or 'RESPAWNING'.
        start_pos: Alias for the initial position, used for respawn targeting.
        respawn_time_at: Monotonic timestamp when RESPAWNING ends.
        coefecient: Controls how often the ghost chases vs. moves randomly.
    """

    def __init__(
        self, pos: tuple[int, int], direction: str | None
    ) -> None:
        """Initialize the ghost's spawn position and state.

        Args:
            pos: A (x, y) tuple of integers for the starting grid position.
            direction: Initial direction string, or None.
        """
        super().__init__(pos, direction)
        self.spawn_pos = self.pos
        self.state = DANGEROUS
        self.start_pos: tuple[int, int] | None = None
        self.respawn_time_at = 0.0
        self.coefecient = 4

    def run_away(
        self, maze: Maze, player_pos: tuple[int, int]
    ) -> tuple[int, int] | None:
        """Choose a neighboring cell farthest from the player.

        Args:
            maze: The Maze instance used for pathfinding.
            player_pos: The (x, y) tuple of the player's current cell.

        Returns:
            The (x, y) tuple of the chosen neighbor, or None if unavailable.
        """
        neighbors = maze.get_neighbors(self.pos)

        if len(neighbors) >= 2:
            valid_neighbors = [
                neighbor for neighbor in neighbors
                if len(maze.get_neighbors(neighbor)) > 1
            ]

            if not valid_neighbors:
                valid_neighbors = neighbors

            previous_fix = [
                neighbor for neighbor in valid_neighbors
                if neighbor != self.previous_pos
            ]

            if previous_fix:
                valid_neighbors = previous_fix
        else:
            valid_neighbors = neighbors

        chosen_neighbor: tuple[int, int] | None = None
        greatest_distance = -1

        for neighbor in valid_neighbors:
            path = maze.find_shortest_path(neighbor, player_pos)

            if len(path) < 2:
                continue

            distance = len(path)
            if distance > greatest_distance:
                chosen_neighbor = neighbor
                greatest_distance = distance
        return chosen_neighbor

    def choose_direction(
        self, maze: Maze, player_pos: tuple[int, int]
    ) -> bool:
        """Choose the next movement direction based on the ghost's state.

        Args:
            maze: The Maze instance used for pathfinding and neighbor lookups.
            player_pos: The (x, y) tuple of the player's current cell.

        Returns:
            True if a direction was chosen, False otherwise.
        """
        if self.target_pos is not None:
            return False

        if self.state == "DANGEROUS":
            if self.moves % self.coefecient == 0:
                nieghbors = maze.get_neighbors(self.pos)
                if nieghbors:
                    next_pos = random.choice(nieghbors)
                else:
                    self.direction = None
                    return False
            else:
                path = maze.find_shortest_path(self.pos, player_pos)

                if len(path) < 2:
                    self.direction = None
                    return False
                next_pos = path[1]

        elif self.state == "EDIBLE":
            edible_next = self.run_away(maze, player_pos)
            if edible_next is None:
                return False
            next_pos = edible_next

        elif self.state == "RESPAWNING":
            return False
        else:
            return False

        dx = next_pos[0] - self.pos[0]
        dy = next_pos[1] - self.pos[1]

        for name, info in DIRECTIONS.items():
            if ((info[0], info[1]) == (dx, dy)):
                self.direction = name
                return True
        return False
