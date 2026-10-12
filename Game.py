from maze import Maze
from Caracter import Player, Ghost


CELL = 80


class Game:

    def __init__(self, width=15, height=15, perfect=False, seed=42):

        self.width = width
        self.height = height
        self.seed = seed
        self.start = (width // 2, height // 2)
        # x_pix and y_pix
        self.start_pix = (((width// 2) * CELL) + CELL // 2, (height // 2) * CELL + CELL // 2 )
        self.player_position = self.start
        self.corners = [(0, 0), (width - 1, height - 1), (width - 1, 0), (0, height - 1)]
        self.maze = Maze(width, height, perfect,seed)
        self.grid = self.maze.grid
        self.player = Player((width // 2, height // 2), None)
        self.ghosts = [Ghost((0, 0), None), Ghost((width - 1, height - 1), None),
            Ghost((width - 1, 0), None), Ghost((0, height - 1), None)]

        self.gums = self.gums_placement()
        self.super_gums = self.super_gums()

        self.visited = set()
        self.lives = 3
        self.score = 0
        self.stop = False

        self.game_over = False




    def gums_placement(self):
        gums = set()
        # print("the start is :", self.start)

        reachable = self.maze.get_reachable_cells(self.start)


        # print(self.grid)
        for i in range(self.width):
            for item in range(self.height):
                cell = (i, item)
                
                if cell in reachable and cell not in self.corners and cell != self.start:
                    gums.add(cell)

        
        return gums


    def super_gums(self):
        return set(self.corners)
    
    def collect_gums(self):
        # visited = set()
        if self.player.target_pos is not None:
            return
        if self.player.pos not in self.visited:

            if self.player.pos in self.gums:
                self.score += 10
                self.visited.add(self.player.pos)
                self.gums.remove(self.player.pos)
            elif self.player.pos in self.super_gums:
                self.score += 50
                self.visited.add(self.player.pos)
                self.super_gums.remove(self.player.pos)
    

    def detect_collision(self):
        for g in self.ghosts:
            dx = self.player.x_pix - g.x_pix
            dy = self.player.y_pix - g.y_pix
            collision =  dx * dx + dy * dy <= (20 + 20) ** 2
            if collision:
                return g
        return None

    def handle_collisions(self):
        g = self.detect_collision()
        if  g is not None:
            if g.state == "DANGEROUS":
#                 if self.lives <= 0:
#                     self.game_over = True
                    # return
                self.lives -= 1
                if self.lives == 0:
                    self.game_over = True
                    return
                self.player.pos = self.start
                self.player.target_pos = None
                self.player.direction = None
                self.player.requested_direction = None

                self.player.x_pix = self.player.pos[0] * CELL + CELL / 2
                self.player.y_pix = self.player.pos[1] * CELL + CELL / 2

                for i, gos in enumerate(self.ghosts):
                    gos.pos = self.corners[i]
                    gos.x_pix = gos.pos[0] * CELL + CELL / 2
                    gos.y_pix = gos.pos[1] * CELL + CELL / 2
                    gos.target_pos = None
                    gos.direction = None
            # elif g.state == "EDIBLE":
                