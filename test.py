import pygame


WIDTH = 1280
HEIGHT = 720
FPS = 60
STEP = 40


BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
BLUE: tuple[int, int, int] = (33, 33, 222)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde


def draw_pacman():
    pass


def build_walls():

    walls = pygame.Surface((WIDTH, HEIGHT))
    walls.fill(BLACK)
    pygame.draw.rect(walls, WHITE, (100, 100, 400, 1))
    # pygame.draw.rect(walls, WHITE, (100, 100, 1, 300))
    # pygame.draw.rect(walls, WHITE, (700, 200, 300, 300), 4, 15)
    return walls


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PAC-MAN")
    clock = pygame.time.Clock()

    walls = build_walls()
    # ghost_rect = pygame.Rect(0, 0, 30, 30)
    running = True

    x = int(WIDTH/2)
    y = int(HEIGHT/2)

    player_rect = pygame.Rect(x, y, WIDTH, HEIGHT)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y -= STEP
                if event.key == pygame.K_DOWN:
                    y += STEP
                if event.key == pygame.K_LEFT:
                    x -= STEP
                if event.key == pygame.K_RIGHT:
                    x += STEP

        if x > WIDTH:
            x = 0
        if x < 0:
            x = WIDTH

        if y > HEIGHT:
            y = 0
        if y < 0:
            y = HEIGHT

        player_rect.move_ip(10, 10)

        screen.fill((0, 0, 0))

        screen.blit(walls, (0, 0))

        pygame.draw.circle(screen, ORANGE, (x, y), 20, 0)
        pygame.draw.circle(screen, WHITE, (360, 300), 4)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()
