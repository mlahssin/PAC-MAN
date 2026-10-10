from maze import Maze
from Caracter import Player, Ghost

class Game:
    def __init__(self, width=15, height=15,perfect, seed=42):
        self.width = width
        self.height = height
        self.seed = seed
        self.player_position = (width // 2, height // 2)
        self.corners = [(0, 0), (width - 1, height - 1), (width - 1, 0), (0, height - 1)]
        self.maze = Maze(width, height, perfect,seed)
        self.grid = self.maze.grid
        self.player = Player((width // 2, height // 2), None, 2)
        self.ghosts = [Ghost((0, 0), None, 2), Ghost((width - 1, height - 1), None, 2)
            Ghost((width - 1, 0), None, 2), Ghost(0, height - 1), None, 2]


        self.gums = set()
        self.super_gums = set()

    
    def gums_placement(self):
        gums = set()
        reachable = self.maze.get_reachable_cells(self.start)
        for cell in self.gird:
            if cell in reachable and not in self.corners:
                gums.add(cell)
        return gums
    
    def super_gums(self):
        return self.corners
            

        

