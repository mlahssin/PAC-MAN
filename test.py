import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN")

running = True

x = int(WIDTH/2)
y = int(HEIGHT/2)

while running:

    for event in pygame.event.get():
        print("Event:", event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            y -= 80

    # DRAW
    
    pygame.draw.circle(screen, (0, 255, 0), (x, y), 20, 0)
    pygame.display.flip()


pygame.quit()
