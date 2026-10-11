import pygame
from mazegenerator import MazeGenerator
from maze import Maze
from Game import Game

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
BLUE: tuple[int, int, int] = (33, 33, 222)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde


ROWS = 31
COLS = 21

CELL = 80

SEED = 42

WIDTH = ROWS * CELL
HEIGHT = COLS * CELL

PADDING = 40

LINE = 2

FPS = 60
STEP = 40


class Visual:

    def __init__(self):

        self.cell = 40
        self.game = Game(ROWS, COLS, perfect=False, seed=SEED)
        (self.center_x, self.center_y) = self.game.start

    def load_maze(self):
        return self.game.grid

    def has_wall(self, cell, side):
        return (cell & side) != 0

    def draw_player(self, maze_sur):

        pygame.draw.circle(maze_sur, ORANGE, ((ROWS * CELL) / 2, (COLS * CELL) / 2 + CELL/2), 20)

    def draw_supergums(self, maze_sur):

        for (x, y) in self.game.corners:
            x_position = (x * CELL) + (CELL / 2)
            y_position = (y * CELL) + (CELL / 2)
            pygame.draw.circle(maze_sur, YELLOW, (x_position, y_position), 10)

    def draw_gums(self, maze_sur):

        maze = self.load_maze()

        gum_placememt = self.game.gums_placement()

        for row, line in enumerate(maze):
            for col, cell in enumerate(line):
                if (col, row) in gum_placememt:
                    pygame.draw.circle(maze_sur, WHITE, ((col * CELL * 2 + CELL) / 2, (row * CELL * 2 + CELL) / 2), 2)

    def draw_42(self):
        print("Reachable cells")
        for item in self.game.maze.get_reachable_cells(self.game.start):
            print(item)

    def draw_maze(self, maze_sur, ROWS, COLS, SEED):

        maze = self.load_maze()

        for row, line in enumerate(maze):
            for col, cell in enumerate(line):

                left = CELL * col
                top = CELL * row
                right = left + CELL
                bottom = top + CELL

                if self.has_wall(cell, 1):
                    pygame.draw.line(maze_sur, WHITE, (left, top), (right, top), 2)
                if self.has_wall(cell, 2):
                    pygame.draw.line(maze_sur, WHITE, (right, top), (right, bottom), 2)
                if self.has_wall(cell, 4):
                    pygame.draw.line(maze_sur, WHITE, (left, bottom), (right, bottom), 2)
                if self.has_wall(cell, 8):
                    pygame.draw.line(maze_sur, WHITE, (left, top), (left, bottom), 2)

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((WIDTH + 2 * PADDING, HEIGHT + 2 * PADDING))
        maze_sur = pygame.Surface((WIDTH + 2, HEIGHT + 2))

        pygame.display.set_caption("PAC-MAN")
        clock = pygame.time.Clock()

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_maze(maze_sur, ROWS, COLS, SEED)

            self.draw_gums(maze_sur)
            self.draw_supergums(maze_sur)

            self.draw_player(maze_sur)

            screen.blit(maze_sur, (PADDING, PADDING))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


def main():
    app = Visual()
    app.run()
    app.draw_42()


main()