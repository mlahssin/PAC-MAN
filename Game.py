from maze import Maze
from Caracter import Player, Ghost

class Game:

    def __init__(self, width=15, height=15, perfect=False, seed=42):

        self.width = width
        self.height = height
        self.seed = seed
        self.start = (width // 2, height // 2)
        self.player_position = self.start
        self.corners = [(0, 0), (width - 1, height - 1), (width - 1, 0), (0, height - 1)]
        self.maze = Maze(width, height, perfect,seed)
        self.grid = self.maze.grid
        self.player = Player((width // 2, height // 2), None, 2)
        self.ghosts = [Ghost((0, 0), None, 2), Ghost((width - 1, height - 1), None, 2),
            Ghost((width - 1, 0), None, 2), Ghost((0, height - 1), None, 2)]

        self.gums = set()
        self.super_gums = set()



    def gums_placement(self):
        gums = set()
        # print("the start is :", self.start)

        reachable = self.maze.get_reachable_cells(self.start)


        # print(self.grid)
        for i in range(self.width):
            for item in range(self.height):
                cell = (i, item)
                
                if cell in reachable and cell not in self.corners and cell != self.start:
                    # print("cell", cell)
                    gums.add(cell)


        return gums


    def super_gums(self):
        return self.corners
            

        