from mazegenerator import MazeGenerator
import time
import random
from maze import Maze
DANGEROUS = "DANGEROUS"
EDIBLE = "EDIBLE"
RESPAWNING = "RESPAWNING"
CELL = 80

pixel_step = CELL / 10

opposite = {
    "up" : "down",
    "down": "up",
    "left":"right",
    "right":"left"
}

modes = {DANGEROUS, EDIBLE, RESPAWNING}
DIRECTIONS = {
    "up": (0, -1, 1, 4),
    "down": (0, 1, 4, 1),
    "left": (-1, 0, 8, 2),
    "right": (1, 0, 2, 8),
}
class Character:
    def __init__(self, pos, direction):
        if (
            not isinstance(pos, tuple)
            or len(pos) != 2
            or not isinstance(pos[0], int)
            or not isinstance(pos[1], int)
        ):
            raise TypeError("pos must be a tuple of two integers (x, y)")

        self.pos = pos

        self.x_pix = (pos[0] * CELL) + CELL / 2
        self.y_pix = (pos[1] * CELL)  + CELL / 2
        
        self.direction = direction
        # i should protect it to be strictement positive
        self.frames_per_cell = 16
        if self.frames_per_cell <= 0:
            raise ValueError("the frame cell must be non negative")

        # if speed <= 0:
            # raise ValueError("Speed must be greater than zero")
        self.target_pos = None
        self.moves = 0
        self.previous_pos = None
        # self.speed = speed
    
    def start_move(self, maze):
        if self.target_pos is not None:
            return False
        if not maze.can_move(self.pos, self.direction):
            return False
        
        direction = DIRECTIONS[self.direction]

        
        dx , dy = direction[0], direction[1]
        x, y = self.pos

        # target_x_pix = (x + dx) * CELL + CELL / 2
        # target_y_pix = (y + dy) * CELL + CELL / 2
        # if self.direction == "left":
        #     self.x_pix -= pixel_step
        # elif self.direction == "right":
        #     self.x_pix += pixel_step
        # elif self.direction == "up":
        #     self.y_pix -= pixel_step
        # elif self.direction == "down":
        #     self.y_pix += pixel_step
        
        # if self.x_pix == target_x_pix and self.y_pix == target_y_pix: 
        self.target_pos = (x + dx, y + dy)

        # self.move_progress = 0.0
        return True

    def update(self, maze):
        
        # if dt < 0:
        #     raise ValueError("the dt must be non negative")
        

        # remaining_distance = self.speed * dt

        

        

        # while remaining_distance > 0:


        if self.target_pos is None:
            if self.direction is None:
                return False
            
            self.start_move(maze)

            if self.target_pos is None:
                return False
        
        tx, ty = self.target_pos
        target_x_pix = tx * CELL + CELL / 2
        target_y_pix = ty * CELL + CELL / 2

        x, y = self.pos

        x_p = x * CELL + CELL / 2
        y_p = y * CELL + CELL / 2


        x_diff = (target_x_pix - x_p) / self.frames_per_cell
        y_diff = (target_y_pix - y_p) / self.frames_per_cell


        self.x_pix += x_diff
        self.y_pix += y_diff

    # Moving right or left: stop at the target.
        if x_diff > 0 and self.x_pix >= target_x_pix:
            self.x_pix = target_x_pix
        elif x_diff < 0 and self.x_pix <= target_x_pix:
            self.x_pix = target_x_pix       
        
        if y_diff > 0 and self.y_pix >= target_y_pix:
            self.y_pix = target_y_pix
        elif y_diff < 0 and self.y_pix <= target_y_pix:
            self.y_pix = target_y_pix
            
        if self.x_pix == target_x_pix and self.y_pix == target_y_pix:
            self.previous_pos = self.pos
            self.pos = tx, ty
            self.moves += 1
            self.target_pos = None


        
        return True
            






class Player(Character):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)
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

        if self.target_pos is not None:
            if self.direction == opposite[self.requested_direction]:
                self.pos, self.target_pos = self.target_pos, self.pos
                self.direction = self.requested_direction
            return

        if maze.can_move(self.pos, self.requested_direction):
            self.direction = self.requested_direction

    

    
    




        



        

        
        

        


class Ghost(Character):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)
        self.spawn_pos = self.pos
        # self.state = EDIBLE

        self.state = DANGEROUS
        self.start_pos = None
        self.respawn_time_at = 0.0

    def run_away(self, maze, player_pos):

        neighbors = maze.get_neighbors(self.pos)

        
        if len(neighbors) >= 2:
            valid_neighbors = [neighbor for neighbor in neighbors
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
        if self.target_pos is not None:
            return False
        
        if self.state == "DANGEROUS":
            if self.moves % 4 == 0:
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
        
        
            

        dx = next_pos[0] - self.pos[0]
        dy = next_pos[1] - self.pos[1]

        for name , info in DIRECTIONS.items():
            if ((info[0], info[1]) == (dx, dy)):
                self.direction = name
                return True


        

        
    



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