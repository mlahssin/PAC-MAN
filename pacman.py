import pygame

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
BLUE: tuple[int, int, int] = (33, 33, 222)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde


# 15 x 7

CELL = 80

MAZE: list[str] = [
    "###############",
    "#.....#.......#",
    "#.###.#.#####.#",
    "#.............#",
    "#.###.###.###.#",
    "#.....#.......#",
    "###############",
]


ROWS = len(MAZE[0])
COLS = len(MAZE)

M_WIDTH = CELL * ROWS
M_HIGHT = CELL * COLS

W_WIDTH = M_WIDTH + 30
W_HIGHT = M_HIGHT + 30


def draw_walls():

    walls = pygame.Surface((M_WIDTH, M_HIGHT))
    walls.fill(BLACK)

    y = 0

    for row in MAZE:
        x = 0
        for cell in row:
            if cell == '#':
                pygame.draw.rect(walls, RED, (x, y, CELL, 1))
            x += CELL
        y += CELL

    return walls


def is_free(col, row):
    if 0 <= col <= COLS and 0 <= row <= ROWS:
        return MAZE[col][row] != '#'
    return False


def main():

    pygame.init()
    running = True


    screen = pygame.display.set_mode((W_WIDTH, W_WIDTH))
    pygame.display.set_caption("PAC-MAN")

    walls = draw_walls()

    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(walls, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



main()
