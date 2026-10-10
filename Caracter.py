from mazegenerator import MazeGenerator
import time
from maze import Maze
DANGEROUS = "DANGEROUS"
EDIBLE = "EDIBLE"
RESPAWNING = "RESPAWNING"

modes = {DANGEROUS, EDIBLE, RESPAWNING}
DIRECTIONS = {
    "up": (0, -1, 1, 4),
    "down": (0, 1, 4, 1),
    "left": (-1, 0, 8, 2),
    "right": (1, 0, 2, 8),
}
class Character:
    def __init__(self, pos, direction, speed):
        if (
            not isinstance(pos, tuple)
            or len(pos) != 2
            or not isinstance(pos[0], int)
            or not isinstance(pos[1], int)
        ):
            raise TypeError("pos must be a tuple of two integers (x, y)")

        self.pos = pos
        self.direction = direction

        if speed <= 0:
            raise ValueError("Speed must be greater than zero")

        self.speed = speed
        self.move_interval = 1 / self.speed
        self.time_since_last_move = 0.0

    def update(self, dt, maze):
        pass


# perf_counter()


class Player(Character):
    def __init__(self, pos, direction, speed):
        super().__init__(pos, direction, speed)
        self.requested_direction = None
    def request_direction(self, direction):
        if not isinstance(direction, str):
            raise TypeError("direction must be a string")
        if direction.lower() not in DIRECTIONS:
            raise ValueError("invalid direction")
        self.requested_direction = direction.lower()

        
        

    def choose_direction(self, maze):
        if self.requested_direction is None:
            return 

        if maze.can_move(self.pos, self.requested_direction):
            self.direction = self.requested_direction
    
    




        



        

        
        

        


class Ghost(Character):
    def __init__(self, pos, direction, speed):
        super().__init__(pos, direction, speed)
        self.spawn_pos = self.pos
        self.state = DANGEROUS
        self.respawn_time_remaining = 0.0

    def choose_direction(self, maze, player_pos):
        pass
    



if __name__ == "__main__":
    m1 = Maze(15, 15, 42)



    if m1.validate_spawns():
        print("the spawns are validated succesfully")
        p1 = Player((m1.width // 2, m1.height // 2), None, 2)
        print(p1.pos)
    else:
        print("one of the spawn are not reachable")


# p1 = Player((0, 0), None, 2)
# p1.request_direction("down")
# p1.choose_direction(m1)

# print(m1.grid[0][0])

# print(p1.update(0.5,m1))
# print(p1.update(0.2,m1))
# print(p1.update(0.2,m1))
# print(p1.update(0.2,m1))


# from math import isclose


# if __name__ == "__main__":
#     maze = Maze(3, 2, 42)

#     # Test 1: two open passages to the right.
#     # 13: walls up/down/left; 5: up/down; 7: up/down/right.
#     maze.grid = [
#         [13, 5, 7],
#         [15, 15, 15],
#     ]
#     player = Player((0, 0), "right", 2)

#     assert player.update(1.2, maze) is True
#     assert player.pos == (2, 0)
#     assert isclose(player.time_since_last_move, 0.2, abs_tol=1e-9)
#     print("PASS: two steps and leftover time")

#     # Test 2: one open passage, then a wall.
#     maze.grid = [
#         [13, 7, 15],
#         [15, 15, 15],
#     ]
#     player = Player((0, 0), "right", 2)

#     assert player.update(1.2, maze) is True
#     assert player.pos == (1, 0)
#     assert player.time_since_last_move == 0.0
#     print("PASS: stops at wall after one step")

#     # Test 3: not enough time for a step.
#     player = Player((0, 0), "right", 2)

#     assert player.update(0.3, maze) is False
#     assert player.pos == (0, 0)
#     assert isclose(player.time_since_last_move, 0.3, abs_tol=1e-9)
#     print("PASS: waits until enough time")

#     # Test 4: blocked from the beginning.
#     player = Player((1, 0), "right", 2)

#     assert player.update(1.2, maze) is False
#     assert player.pos == (1, 0)
#     assert player.time_since_last_move == 0.0
#     print("PASS: blocked without movement")

#     print("ALL CHECKS PASSED")