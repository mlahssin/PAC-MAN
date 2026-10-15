
import random

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
    """Represent a character with grid-based and pixel-based movement."""

    def __init__(self, pos, direction):
        """Initialize the character's position, direction, and movement."""
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

        self.target_pos = None
        self.moves = 0
        self.previous_pos = None

    def start_move(self, maze):
        """Start moving toward the next accessible cell."""
        if self.target_pos is not None:
            return False

        if not maze.can_move(self.pos, self.direction):
            return False

        direction = DIRECTIONS[self.direction]

        dx, dy = direction[0], direction[1]
        x, y = self.pos

        self.target_pos = (x + dx, y + dy)
        return True

    def update(self, maze):
        """Update pixel movement and finalize completed cell transitions."""

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
    """Represent the player and manage requested movement directions."""

    def __init__(self, pos, direction):
        """Initialize the player with no pending direction request."""
        super().__init__(pos, direction)
        self.requested_direction = None

    def request_direction(self, direction):
        """Validate and store the player's requested direction."""
        if not isinstance(direction, str):
            raise TypeError("direction must be a string")

        direction = direction.lower()

        if direction not in DIRECTIONS:
            raise ValueError("direction must be up, down, left, or right")

        self.requested_direction = direction

    def choose_direction(self, maze):
        """Apply the requested direction when movement allows it."""
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
    """Represent a ghost with chasing, fleeing, and respawning behavior."""

    def __init__(self, pos, direction):
        """Initialize the ghost's spawn position and state."""
        super().__init__(pos, direction)
        self.spawn_pos = self.pos
        self.state = DANGEROUS
        self.start_pos = None
        self.respawn_time_at = 0.0
        self.coefecient = 4

    def run_away(self, maze, player_pos):
        """Choose a neighboring cell farthest from the player."""
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

        chosen_neighbor = None
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

    def choose_direction(self, maze, player_pos):
        """Choose the next movement direction based on the ghost's state."""
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
            next_pos = self.run_away(maze, player_pos)

            if next_pos is None:
                return False

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
