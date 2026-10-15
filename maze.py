from mazegenerator import MazeGenerator

from collections import deque


DIRECTIONS = {
    "up": (0, -1, 1, 4),
    "down": (0, 1, 4, 1),
    "left": (-1, 0, 8, 2),
    "right": (1, 0, 2, 8),
}


class Maze:
    """Represent a maze and provide navigation utilities."""

    def __init__(self, width, height, perfect, seed):
        """Generate a maze with the given dimensions and seed."""

        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Maze width and height must be integers.")

        if width < 2 or height < 2 or width > 65 or height > 35:
            raise ValueError(
                "Invalid maze dimensions: width must be between 2 and 65, "
                "and height must be between 2 and 35."
            )
        if not isinstance(seed, int):
            raise TypeError("Maze seed must be an integer.")
        if seed < 0:
            raise ValueError("Maze seed must be a non-negative integer.")
        self.width = width
        self.height = height
        self.seed = seed
        self.grid = MazeGenerator(
            size=(width, height),
            perfect=perfect,
            seed=seed,
        ).maze

    def is_inside(self, pos):
        """Check whether a position is inside the maze boundaries."""
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def can_move(self, pos, direction):
        """Check whether movement is allowed without crossing walls."""
        if (
            not isinstance(pos, tuple) or len(pos) != 2
            or not isinstance(pos[0], int)
            or not isinstance(pos[1], int)
        ):
            raise TypeError("pos must be a tuple of two integers (x, y)")
        if not isinstance(direction, str) or direction not in DIRECTIONS:
            return False
        x, y = pos
        direction_info = DIRECTIONS[direction]
        dx, dy = direction_info[0], direction_info[1]
        if not self.is_inside((x, y)) or not self.is_inside((x + dx, y + dy)):
            return False

        if (
            self.grid[y][x] & direction_info[2] != 0
            or self.grid[y + dy][x + dx] & direction_info[3] != 0
        ):
            return False
        return True

    def get_neighbors(self, pos):
        """Return all accessible neighboring cells of a position."""
        if (
            not isinstance(pos, tuple) or len(pos) != 2
            or not isinstance(pos[0], int)
            or not isinstance(pos[1], int)
        ):
            raise TypeError("pos must be a tuple of two integers (x, y)")

        if not self.is_inside(pos):
            return []

        neighbors = []
        x, y = pos
        for direction in DIRECTIONS:
            if self.can_move(pos, direction):
                dx, dy = DIRECTIONS[direction][0], DIRECTIONS[direction][1]
                neighbors.append((x + dx, y + dy))
        return neighbors

    def get_reachable_cells(self, start):
        """Find all cells reachable from a starting position using BFS."""
        if (
            not isinstance(start, tuple) or len(start) != 2
            or not isinstance(start[0], int)
            or not isinstance(start[1], int)
        ):
            raise TypeError("start must be a tuple of two integers (x, y)")

        if not self.is_inside(start):
            return set()
        x, y = start

        if self.grid[y][x] == 15:
            return set()
        queue = deque([start])
        reachable_cells = {start}

        while queue:

            pos = queue.popleft()
            neighbors = self.get_neighbors(pos)

            for neighbor in neighbors:
                if neighbor not in reachable_cells:
                    reachable_cells.add(neighbor)
                    queue.append(neighbor)
        return reachable_cells

    def get_42_cells(self):
        """Return the positions of all fully walled cells."""
        closed_cells = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 15:
                    closed_cells.add((x, y))
        return closed_cells

    def validate_spawns(self):
        """Check whether the center and four corners are reachable."""
        centre = (self.width // 2, self.height // 2)
        corner1 = (0, 0)
        corner2 = (self.width - 1, self.height - 1)
        corner3 = (0, self.height - 1)
        corner4 = (self.width - 1, 0)
        reachable = self.get_reachable_cells(centre)

        return (centre in reachable
                and corner1 in reachable and corner2 in reachable
                and corner3 in reachable and corner4 in reachable)

    def start_reachable_cells(self, start):
        """Return all cells reachable from the given starting position."""
        return self.get_reachable_cells(start)

    def find_shortest_path(self, start, goal):
        """Find the shortest path between two cells using BFS."""
        visited = {start}
        predecessor = {}

        predecessor[start] = None
        queue = deque([start])

        while queue:

            element = queue.popleft()

            neighbors = self.get_neighbors(element)

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    predecessor[neighbor] = element

            if goal in neighbors:
                break

        if goal not in predecessor:
            return []
        path = []
        cell = goal
        while cell is not None:
            path.append(cell)
            cell = predecessor[cell]
        return path[::-1]
