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


ROWS = 23
COLS = 21

CELL = 80

SEED = 45

WIDTH = ROWS * CELL
HEIGHT = COLS * CELL

PADDING = 40
GAP = 20
SIDEBAR_WIDTH = 1000

WINDOW_WIDTH = PADDING + WIDTH + GAP + SIDEBAR_WIDTH + PADDING
WINDOW_HEIGHT = PADDING + HEIGHT + PADDING

FPS = 60
STEP = 40


class Visual:

    def __init__(self):

        self.cell = 40
        self.game = Game(ROWS, COLS, perfect=False, seed=SEED)
        (self.center_x, self.center_y) = self.game.player_position

    def load_maze(self):
        return self.game.grid

    def has_wall(self, cell, side):
        return (cell & side) != 0

    # def draw_player(self, maze_sur):

    #     col = (ROWS - 1) // 2
    #     row = (COLS - 1) // 2

    #     x = col * CELL + CELL // 2
    #     y = row * CELL + CELL // 2

    #     pygame.draw.circle(maze_sur, ORANGE, (x, y), 20)
    def draw_player(self, maze_sur):
        player = self.game.player

        pygame.draw.circle(
            maze_sur,
            ORANGE,
            (round(player.x_pix), round(player.y_pix)),
            20,
        )

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
            x_position = (x * CELL) + (CELL / 2)
            y_position = (y * CELL) + (CELL / 2)
            pygame.draw.circle(maze_sur, YELLOW, (x_position, y_position), 10)

    # def draw_gums(self, maze_sur):

    #     gum_placememt = self.game.gums

    #     for (col, row) in gum_placememt:
    #         pygame.draw.circle(maze_sur, WHITE, ((col * CELL * 2 + CELL) / 2, (row * CELL * 2 + CELL) / 2), 2)

    def draw_gums(self, maze_sur):

        maze = self.load_maze()

        gum_placememt = self.game.gums

        for row, line in enumerate(maze):
            for col, cell in enumerate(line):
                if (col, row) in gum_placememt:
                    pygame.draw.circle(maze_sur, WHITE, ((col * CELL + CELL / 2, row * CELL + CELL / 2)), 2)

    def draw_42_cells(self, maze_sur):

        cells_42 = self.game.maze.get_42_cells()

        for (col, row) in cells_42:
            pygame.draw.rect(maze_sur, BLUE, (col * CELL, row * CELL, CELL, CELL))

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

        pygame.draw.rect(sidebar_sur, BLUE, (0, 0, SIDEBAR_WIDTH, HEIGHT), 2, 15)

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        maze_sur = pygame.Surface((WIDTH + 2, HEIGHT + 2))
        sidebar_sur = pygame.Surface((SIDEBAR_WIDTH, HEIGHT))

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

            # 1. Update player
            player.update(self.game.maze)

            # 2. Collect gums
            self.game.collect_gums()

            # 3. Update edible timer
            self.game.ghost_update()


            # 4. Update ghosts
            for ghost in self.game.ghosts:
                ghost.choose_direction(self.game.maze, self.game.player.pos)
                ghost.frames_per_cell = 24
                ghost.update(self.game.maze)

            # 5. Check collisions
            self.game.handle_collisions()

            if self.game.game_over:
                print("Game oveeeeeeeeeeeeeeeeeeeer!!!!!")

            

            # self.game.ghost_update()

            maze_sur.fill(BLACK)
            screen.fill(BLACK)


            ##### ayouuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
            self.draw_42_cells(maze_sur)

            self.draw_maze(maze_sur, ROWS, COLS, SEED)

            self.draw_gums(maze_sur)
            self.draw_supergums(maze_sur)

            self.draw_player(maze_sur)
            self.draw_ghosts(maze_sur)
            # self.ghosts(maze_sur)

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