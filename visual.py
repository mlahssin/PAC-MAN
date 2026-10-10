import pygame
from mazegenerator import MazeGenerator
from maze import Maze
# from Game import Game

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
BLUE: tuple[int, int, int] = (33, 33, 222)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde

ROWS = 15
COLS = 12
CELL = 80

SEED = 42

WIDTH = ROWS * CELL
HEIGHT = COLS * CELL

PADDING = 40


FPS = 60
STEP = 40



# class Visual:


def load_maze(width, height, seed):

    generate = Maze(width, height, perfect=False, seed=seed)

    return generate.grid


def has_wall(cell, side):
    return (cell & side) != 0


def draw_player():
    pass


def draw_gum(maze_sur):

    maze = load_maze(ROWS, COLS, SEED)

    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            pygame.draw.circle(maze_sur, WHITE, ((col * CELL * 2 + CELL) / 2, (row * CELL * 2 + CELL) / 2), 2)


def draw_maze(screen, maze_sur, ROWS, COLS, SEED):

    maze_sur = pygame.Surface((WIDTH + 2, HEIGHT + 2))

    maze = load_maze(ROWS, COLS, SEED)

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

    draw_gum(maze_sur)

    screen.blit(maze_sur, (PADDING, PADDING))


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

        draw_maze(screen, maze_sur, ROWS, COLS, SEED)

        maze = load_maze(ROWS, COLS, SEED)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()
