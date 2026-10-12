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


ROWS = 15

COLS = 15

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
        (self.center_x, self.center_y) = self.game.player_position

    def load_maze(self):
        return self.game.grid

    def has_wall(self, cell, side):
        return (cell & side) != 0

    # def draw_player(self, maze_sur):

    #     pygame.draw.circle(maze_sur, ORANGE, ((ROWS * CELL) / 2, (COLS * CELL) / 2 + CELL/2), 20)

    def draw_player(self, maze_sur):
        player = self.game.player

        pygame.draw.circle(
            maze_sur,
            ORANGE,
            (round(player.x_pix), round(player.y_pix)),
            20,
        )
    def draw_supergums(self, maze_sur):

        for (x, y) in self.game.super_gums:
            x_position = (x * CELL) + (CELL / 2)
            y_position = (y * CELL) + (CELL / 2)
            pygame.draw.circle(maze_sur, YELLOW, (x_position, y_position), 10)

    def draw_gums(self, maze_sur):

        maze = self.load_maze()

        gum_placememt = self.game.gums

        for row, line in enumerate(maze):
            for col, cell in enumerate(line):
                if (col, row) in gum_placememt:
                    pygame.draw.circle(maze_sur, WHITE, ((col * CELL + CELL / 2, row * CELL + CELL / 2)), 2)

    def draw_42(self):
        print("Reachable cells")
        for item in self.game.maze.get_reachable_cells(self.game.player_position):
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
            # dt = clock.tick(60) / 1000



            # print(
            #     "can move down:",
            #     self.game.maze.can_move(self.game.player.pos, "down"),
            # )
            direction = None
            # print("wach ymkn", self.game.maze.can_move(self.game.player.pos, "up"))

            # print("hhhhhhh", dt, self.game.player.pos,
            #     self.game.player.target_pos,
            #     self.game.player.move_progress)
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
            # print("direction is :", direction)
            # print("requested:", repr(self.game.player.requested_direction))
            
            self.game.player.choose_direction(self.game.maze)

            # self.game.player.update(dt, self.game.maze)
            player = self.game.player

            # print("BEFORE:", player.direction, player.pos,
            #     self.game.maze.can_move(player.pos, player.direction))

            moved = player.update(self.game.maze)
            self.game.collect_gums()

            # print("AFTER:", moved, player.pos,
            #     player.target_pos, player.move_progress)
            maze_sur.fill(BLACK)
            screen.fill(BLACK)   
            self.draw_maze(maze_sur, ROWS, COLS, SEED)

            self.draw_gums(maze_sur)
            self.draw_supergums(maze_sur)

            self.draw_player(maze_sur)

            screen.blit(maze_sur, (PADDING, PADDING))
            # print("here\n",
            #     "player_dir\n",self.game.player.direction,
            #     "pl_pos\n",self.game.player.pos,
            #     "pl_tar\n",self.game.player.target_pos,
            #     "pl_prog\n",self.game.player.move_progress,
            # )
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()



def main():
    app = Visual()
    app.run()
    app.draw_42()


main()