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


# class Visual:

#     def __init__(self, game):

#         pygame.init()

#         self.cols = len(game.grid[0])
#         self.rows = len(game.grid)

#         self.width = self.cols * CELL
#         self.height = self.rows * CELL

#         self.screen = pygame.display.set_mode((WIDTH + 2 * PADDING, HEIGHT + 2 * PADDING))

#         self.gums = game.gums_placement()

#         pygame.display.set_caption("PAC-MAN")
#         clock = pygame.time.Clock()


#     def window_size():

#         return (self.width + LINE + 2 * PADDING,
#             self.heigh + LINE + 2 * PADDING)


#     def build_maze_surface(self):

#         surface = pygame.Surface((self.width + LINE, self.heigh))




game = Game(ROWS, COLS, perfect=False, seed=SEED)


(center_x, center_y) = game.player_position


def load_maze():
    return game.maze.grid


def has_wall(cell, side):
    return (cell & side) != 0


# def draw_player(maze_sur):

#     pygame.draw.circle(maze_sur, ORANGE, ((ROWS * CELL) / 2, (COLS * CELL) / 2 + CELL/2), 20)

def draw_player(maze_sur):
    player = game.player
    x, y = player.pos

    if player.target_pos is not None:
        tx, ty = player.target_pos
        x += (tx - x) * player.move_progress
        y += (ty - y) * player.move_progress

    pygame.draw.circle(
        maze_sur,
        ORANGE,
        (round(x * CELL + CELL / 2),
         round(y * CELL + CELL / 2)),
        20,
    )

def draw_supergums(maze_sur):

    for (x, y) in game.corners:
        x_position = (x * CELL) + (CELL / 2)
        y_position = (y * CELL) + (CELL / 2)
        pygame.draw.circle(maze_sur, YELLOW, (x_position, y_position), 10)


def draw_gums(maze_sur):

    maze = load_maze()

    gum_placememt = game.gums_placement()

    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            if (col, row) in gum_placememt:
                # print("GUMS!!!!!")
                pygame.draw.circle(maze_sur, WHITE, ((col * CELL * 2 + CELL) / 2, (row * CELL * 2 + CELL) / 2), 2)


def draw_maze(maze_sur, ROWS, COLS, SEED):

    maze = load_maze()

    pygame.draw.line(maze_sur, RED, (0, CELL * ROWS), (CELL * COLS, CELL * ROWS), 2)

    for row, line in enumerate(maze):
        for col, cell in enumerate(line):

            left = CELL * col
            top = CELL * row
            right = left + CELL
            bottom = top + CELL

            if has_wall(cell, 1):
                pygame.draw.line(maze_sur, WHITE, (left, top), (right, top), 2)
            if has_wall(cell, 2):
                pygame.draw.line(maze_sur, WHITE, (right, top), (right, bottom), 2)
            if has_wall(cell, 4):
                pygame.draw.line(maze_sur, WHITE, (left, bottom), (right, bottom), 2)
            if has_wall(cell, 8):
                pygame.draw.line(maze_sur, WHITE, (left, top), (left, bottom), 2)


def main():

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


        maze_sur.fill(BLACK)
        screen.fill(BLACK)


        draw_maze(maze_sur, ROWS, COLS, SEED)

        draw_gums(maze_sur)
        draw_supergums(maze_sur)

        draw_player(maze_sur)

        screen.blit(maze_sur, (PADDING, PADDING))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()