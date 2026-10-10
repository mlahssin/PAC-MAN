from mazegenerator import MazeGenerator

from collections import deque


DIRECTIONS = {
    "up": (0, -1, 1, 4),
    "down": (0, 1, 4, 1),
    "left": (-1, 0, 8, 2),
    "right": (1, 0, 2, 8),
}

# opposite = {
#     "up": "down",
#     "down": "up",
#     "left": "right",
#     "right": "left"
# }


class Maze:
    def __init__(self, width, height,perfect, seed):
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("heigh and width must be integers")
        
        if width < 2 or height < 2:
            raise ValueError("the width and the height must be >= 2")
        
        if not isinstance(seed, int):
            raise TypeError("the seed must be an integer")
        if seed < 0:
            raise ValueError("Seed must be nonnegative")
        self.width = width
        self.height = height

        self.seed = seed
        self.grid = MazeGenerator(
            size=(width, height),
            perfect=perfect,
            seed=seed,
        ).maze

    def is_inside(self, pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def can_move(self, pos, direction):
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
        dq = deque([start])
        reachable = {start}

        while dq:
            pos = dq.popleft()
            neighbors = self.get_neighbors(pos)

            for n in neighbors:
                if n not in reachable:
                    reachable.add(n)
                    dq.append(n)
        return reachable

    def validate_spawns(self):
        centre = (self.width // 2, self.height // 2)
        corner1 = (0, 0)
        corner2 = (self.width - 1, self.height - 1)
        corner3 = (0, self.height - 1)
        corner4 = (self.width - 1, 0)
        reachable = self.get_reachable_cells(centre)

        return (centre in reachable
                and corner1 in reachable and corner2 in reachable
                and corner3 in reachable and corner4 in reachable)