import pygame
from mazegenerator import MazeGenerator
from maze import Maze
from Game import Game

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
ORANGE_42: tuple[int, int, int] = (219, 70, 4)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde


#480058

ROWS = 21
COLS = 21

CELL = 80

SEED = 42

WIDTH = ROWS * CELL
HEIGHT = COLS * CELL

PADDING = 40
GAP = 20
SIDEBAR_WIDTH = 800

WINDOW_WIDTH = PADDING + WIDTH + GAP + SIDEBAR_WIDTH + PADDING
WINDOW_HEIGHT = PADDING + HEIGHT + PADDING

FPS = 60
STEP = 40


class Visual:

    def __init__(self):

        self.cell = 40
        self.game = Game(ROWS, COLS, perfect=False, seed=SEED)
        (self.center_x, self.center_y) = self.game.player_position

        self.player_img = None
        self.supergum_img = None
        self.gum_img = None

    def load_maze(self):
        return self.game.grid

    def has_wall(self, cell, side):
        return (cell & side) != 0

    def load_scaled(self, path, size):

        try:
            img = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            return None
        scale = size / max(img.get_width(), img.get_height())
        return pygame.transform.smoothscale(
            img, (round(img.get_width() * scale),
                  round(img.get_height() * scale)))

    def load_images(self):
        self.player_img = self.load_scaled("assets/player.png", CELL - 8)
        self.supergum_img = self.load_scaled("assets/supergum.png", CELL // 2)
        self.gum_img = self.load_scaled("assets/gum.png", CELL // 3)

    def draw_player(self, maze_sur):

        player = self.game.player
        center = (round(player.x_pix), round(player.y_pix))

        if self.player_img is not None:
            rect = self.player_img.get_rect(center=center)
            maze_sur.blit(self.player_img, rect)
        else:
            pygame.draw.circle(maze_sur, ORANGE, center, 20)

    def draw_ghosts(self, maze_sur):
        colors = (RED, PINK, CYAN, ORANGE)

        for i, ghost in enumerate(self.game.ghosts):
            pygame.draw.circle(
                maze_sur,
                colors[i % len(colors)],
                (round(ghost.x_pix), round(ghost.y_pix)),
                20,
            )

    def draw_supergums(self, maze_sur):

        for (x, y) in self.game.super_gums:
            center = (x * CELL + CELL // 2, y * CELL + CELL // 2)

            if self.supergum_img is not None:
                rect = self.supergum_img.get_rect(center=center)
                maze_sur.blit(self.supergum_img, rect)
            else:
                pygame.draw.circle(maze_sur, YELLOW, center, 10)

    def draw_gums(self, maze_sur):

        # maze = self.load_maze()

        # gum_placememt = self.game.gums

        # for row, line in enumerate(maze):
        #     for col, cell in enumerate(line):
        #         if (col, row) in gum_placememt:
        #             pygame.draw.circle(maze_sur, WHITE, ((col * CELL + CELL / 2, row * CELL + CELL / 2)), 4)

        for (col, row) in self.game.gums:
            
            center = (col * CELL + CELL // 2, row * CELL + CELL // 2)

            if self.gum_img is not None:
                rect = self.gum_img.get_rect(center=center)
                maze_sur.blit(self.gum_img, rect)
            else:
                pygame.draw.circle(maze_sur, WHITE, center, 4)

    def draw_42_cells(self, maze_sur):

        cells_42 = self.game.maze.get_42_cells()

        for (col, row) in cells_42:
            pygame.draw.rect(maze_sur, ORANGE_42, (col * CELL, row * CELL, CELL, CELL))

    def ghosts(self, maze_sur):

        for (x, y) in self.game.corners:
            x_position = (x * CELL) + (CELL / 2)
            y_position = (y * CELL) + (CELL / 2)
            pygame.draw.circle(maze_sur, RED, (x_position, y_position), 20)

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

    def draw_maze_side_bar(self, sidebar_sur):

        rect = sidebar_sur.get_rect()

        pygame.draw.rect(sidebar_sur, WHITE, rect, 2,
                         border_top_right_radius=20,
                         border_bottom_right_radius=20)

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.load_images()

        maze_sur = pygame.Surface((WIDTH + 2, HEIGHT + 2), pygame.SRCALPHA)
        sidebar_sur = pygame.Surface((SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA)

        background = pygame.image.load("assets/background.jpeg").convert()
        background = pygame.transform.smoothscale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption("PAC-MAN")
        clock = pygame.time.Clock()

        running = True
        while running:
            direction = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        print("KEYDOWN received:", event.key)
                        direction = "left"   
                    elif event.key == pygame.K_RIGHT:
                        print("KEYDOWN received:", event.key)
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        print("KEYDOWN received:", event.key)
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        direction = "down"
                        print("KEYDOWN received:", event.key)
            if direction is not None:
                self.game.player.request_direction(direction)

            self.game.player.choose_direction(self.game.maze)

            player = self.game.player

            moved = player.update(self.game.maze)

            for ghost in self.game.ghosts:
                ghost.choose_direction(self.game.maze, self.game.player.pos)
                ghost.frames_per_cell = 24
                ghost.update(self.game.maze)
            if not self.game.game_over:

                self.game.handle_collisions()
            if self.game.game_over:
                print("Game oveeeeeeeeeeeeeeeeeeeer!!!!!")

            self.game.collect_gums()

            # maze_sur.fill(BLACK)
            maze_sur.fill((0, 0, 0, 120))
            sidebar_sur.fill((0, 0, 0, 120))

            # screen.fill(BLACK)
            screen.blit(background, (0, 0))

            self.draw_42_cells(maze_sur)

            self.draw_maze(maze_sur, ROWS, COLS, SEED)

            self.draw_gums(maze_sur)
            self.draw_supergums(maze_sur)

            self.draw_player(maze_sur)
            self.draw_ghosts(maze_sur)

            self.draw_maze_side_bar(sidebar_sur)

            screen.blit(maze_sur, (PADDING, PADDING))
            screen.blit(sidebar_sur, (PADDING + WIDTH + GAP, PADDING))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


def main():
    app = Visual()
    app.run()


main()