import pygame

# 7 x 15

CELL = 40

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


def is_free(col, row):
    if 0 <= col <= COLS and 0 <= row <= ROWS:
        return MAZE[col][row] != '#'
    return False


def main():

    pygame.init()
    running = True

    screen = pygame.display.set_mode((W_WIDTH, W_WIDTH))
    pygame.display.set_caption("PAC-MAN")
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



main()
